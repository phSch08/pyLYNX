from ._generic import EulynxGeneric

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

class EulynxSignalLuminosity:
    day = bytes.fromhex('01')
    night = bytes.fromhex('02')
    deleted = bytes.fromhex('FE')

class EulynxSignal(EulynxGeneric):
    protocol_type = bytes.fromhex('30')

    @classmethod
    def indicate_signal_aspect(cls, sender_id : str, receiver_id : str, signal_aspect : bytes) -> bytes:
        '''
        generate command to indicate a signal aspect

        @param sender_id Identifier of the sending instance of the command
        @param receiver_id Identifier of the receiving instance of the command

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

        message += signal_aspect

        message += bytes.fromhex('02')      # extension of basic aspect type
        message += bytes.fromhex('FF')      # speed indicator (FF = intendet dark)
        message += bytes.fromhex('FF')      # speed indicator announcements (FF = intendet dark)
        message += bytes.fromhex('FF')      # direction indicator (FF = intendet dark)
        message += bytes.fromhex('FF')      # direction indicator announcements (FF = intendet dark)
        message += bytes.fromhex('FF')      # downgrade information (FF = not applicable)
        message += bytes.fromhex('FF')      # route information (FF = not applicable)
        message += bytes.fromhex('FF')      # intentionally dark (FF = not applicable)
        message += 9 * bytes.fromhex('00')  # national specified
        
        return message

    @classmethod
    def set_luminosity(cls, sender_id : str, receiver_id : str, luminosity : bytes) -> bytes:
        '''
        generate command to indicate a signal aspect

        @param sender_id Identifier of the sending instance of the command
        @param receiver_id Identifier of the receiving instance of the command

        @returns bytes 
        ''' 
        message = cls.protocol_type        # Protocol Type
        message += bytes.fromhex('0002')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += luminosity
        
        return message