import asyncio
import queue
import grpc
import sys
import logging
import threading

from .proto.rasta_pb2 import SciPacket
from .proto.rasta_pb2_grpc import RastaServicer, add_RastaServicer_to_server

stop_servicer = False

class _RastaElement(RastaServicer):
        def __init__(self, message_queue):
             self.message_queue = message_queue
        
        def Stream(self, request_iterator, context):
            while True:
                if stop_servicer:
                     break
                
                try:
                    logging.warning("Waiting for Message...")
                    message = self.message_queue.get(True, 10)
                    yield SciPacket(message=message)
                    logging.warning("Sent Message...")
                    self.message_queue.task_done()
                except:
                    continue


class pyLYNX:
    def __init__(self, listen_addr: str):
        self.message_queue: queue.Queue = queue.Queue()
        self.listen_addr = listen_addr

    def __enter__(self):
        self.thread = threading.Thread(target=self.do_magic).start()
        return self
         
    def __exit__(self, type, value, traceback):
        logging.warning("Exiting...")
        global stop_servicer
        stop_servicer = True
        self.server.wait_for_termination()

    def do_magic(self):
         asyncio.run(self.start_server())
         
    async def start_server(self):
        self.server = grpc.aio.server()
        rasta_element = _RastaElement(self.message_queue)
        add_RastaServicer_to_server(rasta_element, self.server)
        self.server.add_insecure_port(self.listen_addr)
        logging.warning("Starting Server...")
        await self.server.start()
        await self.server.wait_for_termination()

    def send_message(self, message: bytes):
         self.message_queue.put_nowait(message)