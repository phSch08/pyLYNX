import grpc
import logging
import multiprocessing
import time
import signal
import threading

from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from .messages._generic import EulynxGenericParser
from .proto.rasta_pb2 import SciPacket
from .proto.rasta_pb2_grpc import RastaServicer, add_RastaServicer_to_server

stop_servicer = False
   

class _RastaElement(RastaServicer):
        def __init__(self, message_queue, response_queue):
             self.message_queue = message_queue
             self.response_queue = response_queue

        def message_reader(self, request_iterator):
            for request in request_iterator:
                self.response_queue.put_nowait(request.message)

        def Stream(self, request_iterator, context):
            threading.Thread(target=self.message_reader, args=(request_iterator,)).start()
            while True:
                message = self.message_queue.get(True)
                yield SciPacket(message=message)
                logging.debug(message)
                self.message_queue.task_done()


class pyLYNX:
    def __init__(self, listen_addr: str):
        '''
        Constructor for pyLYNX class

        @param listen_addr IP + Port where the underlying grpc server should listen

        @returns pyLYNX-Object
        '''
        self.message_queue: multiprocessing.JoinableQueue = multiprocessing.JoinableQueue()
        self.response_queue: multiprocessing.JoinableQueue = multiprocessing.JoinableQueue()
        self.listen_addr = listen_addr
        self.parsers = []
        self.default_parser = None

    def __enter__(self):
        self.subprocess = multiprocessing.Process(target=self._serve)
        self.subprocess.start()
        return self
         
    def __exit__(self, type, value, traceback):
        logging.info("Waiting for Message Queue to get empty")
        self.message_queue.join()
        logging.info("Message Queue is empty, killing Background Service")
        self.subprocess.kill()

    def open(self) -> None:
        '''
        Create GRPC server to accept connections.

        @returns None
        '''
        self.__enter__()
    
    def close(self) -> None:
        '''
        Stop the underlying grpc server. Unsend messages will still be processed.

        @returns None
        '''
        self.__exit__()

    def _serve(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.info("Preparing Server...")
        self.server = grpc.server(ThreadPoolExecutor())
        rasta_element = _RastaElement(self.message_queue, self.response_queue)
        add_RastaServicer_to_server(rasta_element, self.server)
        self.server.add_insecure_port(self.listen_addr)
        logging.info("Starting Server...")
        self.server.start()
        logging.info("Server running at " + self.listen_addr)
        self.server.wait_for_termination()

    def send_message(self, message: bytes) -> None:
        '''
        Send the given message

        @param message Message to send

        @returns None
        '''
        self.message_queue.put_nowait(message)

    def register_parser(self, parser: EulynxGenericParser) -> None:
        '''
        Register a message parser that is called when calling the "parse_message" method.

        @parser the parser to register

        @returns None
        '''
        self.parsers.append(parser)

    def register_default_parser(self, parser: EulynxGenericParser) -> None:
        '''
        Register a default parser that will be called in the "parse_message" method
        if no other parser could be found. An existing default parser will be overwritten.

        @parser the default parser to register

        @returns None
        '''
        self.default_parser = parser

    def parse_messages(self) -> None:
        '''
        Parse all messages that have been received since the last call of this function.

        @returns None
        '''
        while not self.response_queue.empty():
            found_parser = False
            request = self.response_queue.get_nowait()
            for parser in self.parsers:
                found_parser = found_parser or parser.parse_message(request)

            if not found_parser and self.default_parser:
                self.default_parser.parse_message(request)
            

            self.response_queue.task_done()
