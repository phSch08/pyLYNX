class EulynxGeneric:
    protocol_type = bytes.fromhex('00')

    @classmethod
    def pdi_version_check(cls, sender_id: str, receiver_id: str) -> bytes:
        message = cls.protocol_type
        message += bytes.fromhex('2400')

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += bytes.fromhex('01')

        return message

    @classmethod
    def initialization_request(cls, sender_id: str, receiver_id: str) -> bytes:
        message = cls.protocol_type
        message += bytes.fromhex('2100')

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        return message
