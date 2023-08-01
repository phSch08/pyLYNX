# pyLYNX
EULYNX implementation for Python

## Installation
Install pylynx using pip:
```
pip install git+https://github.com/phSch08/pyLYNX
```

## Usage
To send EULYNX messages from python an additional RaSTA bridge is required. You can use and adapt the docker-compose file provided in this repository to start the bridge and a simulated signal.

Check out `example.py` to see how to use pyLYNX.

The following example shows, how to send messages with a running RaSTA bridge:

```(python)
from pyLYNX.pyLYNX import pyLYNX

with pyLYNX("<BRIDGE_IP>:<BRIDGE_PORT>") as srv:
    srv.send_message(message)
```

You can generate a message to send with the provided classes `EulynxSignal` and `EulynxPoint`:

### EulynxSignal

__Import__
```(python)
from pyLYNX.messages.signal import EulynxSignal, EULYNXSignalAspect, EulynxSignalLuminosity
```

__PDI Version Check__
```(python)
pdi_version_check(sender_id: str, receiver_id: str)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving signal

__Initialization Request__
```(python)
initialization_request(sender_id: str, receiver_id: str)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving signal

__Indicate Signal Aspect__
```(python)
indicate_signal_aspect(sender_id : str, receiver_id : str, signal_aspect : bytes)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving signal
- `signal_aspect`: signal aspect to display. Use the provided class `EulynxSignalAspect`

```(python)
class EulynxSignalAspect:
    stop_danger = bytes.fromhex('01')
    proceed_clear = bytes.fromhex('04')
    flashing_clear1 = bytes.fromhex('05')
    flashing_clear2 = bytes.fromhex('06')
    approach_caution = bytes.fromhex('07')
    expect_stop = bytes.fromhex('08')
    shunting_allowed = bytes.fromhex('02')
    shunting_allowed2 = bytes.fromhex('09')
    ignore_signal = bytes.fromhex('0A')
```

__Set Luminosity__
```(python)
set_luminosity(sender_id : str, receiver_id : str, luminosity : bytes)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving signal
- `luminosity`: the luminosity of the signal. Use the provided class `EulynxSignalLuminosity`

```(python)
class EulynxSignalLuminosity:
    day = bytes.fromhex('01')
    night = bytes.fromhex('02')
    deleted = bytes.fromhex('FE')
```


### EulynxPoint
__Import__
```(python)
from pyLYNX.messages.point import EulynxPoint, PointPosition
```

__PDI Version Check__
```(python)
pdi_version_check(sender_id: str, receiver_id: str)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving point

__Initialization Request__
```(python)
initialization_request(sender_id: str, receiver_id: str)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving point

__Move Point__
```(python)
move_point(sender_id : str, receiver_id : str, point_position : bytes)
```
- `sender_id`: id of the sending instance (Bridge)
- `receiver_id`: id of the receiving point
- `luminosity`: the position, the point should move to. Use the provided class `PointPosition`

```(python)
class PointPosition:
    right = bytes.fromhex('01')
    left = bytes.fromhex('02')
```
