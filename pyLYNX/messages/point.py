from ._generic import EulynxGeneric

class PointPosition:
    right = bytes.fromhex('01')
    left = bytes.fromhex('02')

class EulynxPoint(EulynxGeneric):
    protocol_type = bytes.fromhex('40')

    @classmethod
    def move_point(cls, sender_id : str, receiver_id : str, point_position : bytes) -> bytes:
        '''
        generate command to switch point to position

        @param sender_id Identifier of the sending instance of the command
        @param receiver_id Identifier of the receiving instance of the 
        @param point_position Position to point should switch to

        @returns bytes 
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