import asyncio
import grpc
import logging
import multiprocessing
import time
import signal

from .proto.rasta_pb2 import SciPacket
from .proto.rasta_pb2_grpc import RastaServicer, add_RastaServicer_to_server

stop_servicer = False
   

class _RastaElement(RastaServicer):
        def __init__(self, message_queue):
             self.message_queue = message_queue
        
        def Stream(self, request_iterator, context):
            logging.warning("Running Stream")
            while True:                
                try:
                    logging.debug("Waiting for Message...")
                    message = self.message_queue.get(True, 60)
                    yield SciPacket(message=message)
                    logging.info("Sent Message...")
                    self.message_queue.task_done()
                except:
                    continue


class pyLYNX:
    def __init__(self, listen_addr: str):
        self.message_queue: multiprocessing.JoinableQueue = multiprocessing.JoinableQueue()
        self.listen_addr = listen_addr

    def __enter__(self):
        self.subprocess = multiprocessing.Process(target=self.prepare_server)
        self.subprocess.start()
        return self
         
    def __exit__(self, type, value, traceback):
        logging.info("Waiting for Message Queue to get empty")
        self.message_queue.join()
        logging.info("Message Queue is empty, killing Background Service")
        self.subprocess.kill()

    def open(self):
        self.__enter__()
    
    def close(self):
        self.__exit__()

    def prepare_server(self):
        logging.info("Preparing Server...")
        time.sleep(2)
        logging.warning(self.message_queue.empty())
        asyncio.run(self.start_server())
         
    async def start_server(self):
        self.server = grpc.aio.server()
        rasta_element = _RastaElement(self.message_queue)
        add_RastaServicer_to_server(rasta_element, self.server)
        self.server.add_insecure_port(self.listen_addr)
        logging.info("Starting Server...")
        await self.server.start()
        await self.server.wait_for_termination()

    def send_message(self, message: bytes):
         self.message_queue.put_nowait(message)