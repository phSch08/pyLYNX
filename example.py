from pyLYNX.messages.signal import EulynxSignal, EulynxSignalAspect
from pyLYNX.pyLYNX import pyLYNX
import time
import asyncio
import logging


async def main():
    with pyLYNX("0.0.0.0:50051") as srv1:
        logging.warning("Sending Init Messages")
        srv1.send_message(EulynxSignal.pdi_version_check("INTERLOCKING", "99N1"))
        srv1.send_message(EulynxSignal.initialization_request("INTERLOCKING", "99N1"))

        for i in range(5):
            if (i % 2):
                logging.warning("Setting to green")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().flashing_clear1))
            else:
                logging.warning("Setting to red")
                srv1.send_message(EulynxSignal.indicate_signal_aspect("INTERLOCKING", "99N1", EulynxSignalAspect().flashing_clear2))

            time.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())