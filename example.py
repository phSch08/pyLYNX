from pyLYNX.messages.signal import EulynxSignal, EulynxSignalAspect
from pyLYNX.pyLYNX import pyLYNX
from pyLYNX.messages._generic import EulynxGenericParser
from pyLYNX.proto.rasta_pb2_grpc import RastaStub
from pyLYNX.proto.rasta_pb2 import SciPacket 
from concurrent.futures import ThreadPoolExecutor
import time
import logging
import sys
import grpc

class DefaultParser(EulynxGenericParser):
    def parse_message(self, message: bytes) -> bool:
        '''
        parse a EULYNX message

        @param message EULYNX message as byte array

        @returns True if the message could be parsed successfully, otherwise False
        '''
        logging.warning(message)
        return True

def print_usage():
    print("""usage: python example.py [mode]

Possible options for MODE argument:
    server      Run as grpc server
    client      Run as grpc client
    """)

def grpc_streamer(message, channel):
    stub = RastaStub(channel)
    response_iterator = stub.Stream(iter((SciPacket(message=message.encode()),)))

    for response in response_iterator:
        print(response.message)


def grpc_client():
    executor = ThreadPoolExecutor()
    with grpc.insecure_channel('localhost:50051') as channel:
        future = executor.submit(grpc_streamer, "Hello World", channel)
        future.result()

def server():
    logging.basicConfig(level="DEBUG")
    with pyLYNX("0.0.0.0:50051") as srv1:
        srv1.register_default_parser(DefaultParser())
        time.sleep(5)
        logging.info("Sending Init Messages")
        srv1.send_message(EulynxSignal.pdi_version_check("INTERLOCKING", "99N1"))
        srv1.send_message(EulynxSignal.initialization_request("INTERLOCKING", "99N1"))

        for i in range(100):
            srv1.parse_messages()
            if (i % 2):
                logging.info("Setting to green")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().proceed_clear))
            else:
                logging.info("Setting to red")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().stop_danger))

            time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
    elif sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client":
        grpc_client()
    else:
        print_usage()