from ._generic import EulynxGeneric, EulynxGenericParser
from typing import Callable


class PointPosition:
    right = bytes.fromhex('01')
    left = bytes.fromhex('02')


class EulynxPoint(EulynxGeneric):
    protocol_type = bytes.fromhex('40')

    @classmethod
    def move_point(cls, sender_id: str, receiver_id: str, point_position: bytes) -> bytes:
        '''
        generate command to switch point to position

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the 
        :param point_position: Position to point should switch to

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0100')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += point_position
        return message


class EulynxPointParser(EulynxGenericParser):
    def __init__(self):
        self.move_point_callbacks = []

    def parse_message(self, message: bytes) -> bool:
        '''
        parse a EULYNX message and call the registered callback functions if the message matches the supported types.

        :param message: EULYNX message as byte array

        returns True if the message could be parsed successfully, otherwise False
        '''
        if (message[:3] == EulynxPoint.protocol_type + bytes.fromhex('0100')):
            for func in self.indicate_signal_aspect_callbacks:
                sender = message[3:23].decode('iso8859-1').rstrip("_")
                receiver = message[23:43].decode('iso8859-1').rstrip("_")
                func[0](sender, receiver, message[43], func[1])
            return True

        return False

    def register_move_point_callback(self, function: Callable[[str, str, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "indicate signal aspect" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, point target position, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.indicate_signal_aspect_callbacks.append((function, tuple))
