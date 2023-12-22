from pyLYNX.messages.signal import EulynxSignal, EulynxSignalAspect
from pyLYNX.pyLYNX import pyLYNX
import time
import asyncio
import logging


async def main():
    logging.basicConfig(level="INFO")
    with pyLYNX("0.0.0.0:50051") as srv1:
        time.sleep(5)
        logging.info("Sending Init Messages")
        srv1.send_message(EulynxSignal.pdi_version_check("INTERLOCKING", "99N1"))
        srv1.send_message(EulynxSignal.initialization_request("INTERLOCKING", "99N1"))

        for i in range(100):
            if (i % 2):
                logging.info("Setting to green")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().proceed_clear))
            else:
                logging.info("Setting to red")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().stop_danger))

            time.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())