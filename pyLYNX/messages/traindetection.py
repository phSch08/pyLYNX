from ._generic import EulynxGeneric, EulynxGenericParser
from typing import Callable


class TrainDetectionFCMode:
    FCU = bytes.fromhex('01')
    FCC = bytes.fromhex('02')
    FCPA = bytes.fromhex('03')
    FCP = bytes.fromhex('04')
    ACKNOWLEDGE = bytes.fromhex('05')


class TrainDetectionOccupancyState:
    VACANT = bytes.fromhex('01')
    OCCUPIED = bytes.fromhex('02')
    DISTURBED = bytes.fromhex('03')
    WAIT_SWEEPING = bytes.fromhex('04')
    WAIT_ACKNOWLEDGMENT = bytes.fromhex('05')
    SWEEPING_DETECTED = bytes.fromhex('06')


class TrainDetectionForceClearAbility:
    UNABLE = bytes.fromhex('01')
    ABLE = bytes.fromhex('02')


class TrainDetectionPOMState:
    OK = bytes.fromhex('01')
    NOK = bytes.fromhex('02')
    NA = bytes.fromhex('FF')


class TrainDetectionDisturbanceState:
    OPERATIONAL = bytes.fromhex('01')
    TECHNICAL = bytes.fromhex('02')
    NA = bytes.fromhex('FF')


class TrainDetectionChangeTrigger:
    PASSING_DETECTED = bytes.fromhex('01')
    EIL_COMMAND = bytes.fromhex('02')
    MAINTAINER_COMMAND = bytes.fromhex('03')
    TECHNICAL_FAILURE = bytes.fromhex('04')
    INITIAL_SECTION = bytes.fromhex('05')
    INTERNAL_TRIGGER = bytes.fromhex('06')
    NA = bytes.fromhex('FF')


class TrainDetectionRejectionReason:
    OPERATIONAL = bytes.fromhex('01')
    TECHNICAL = bytes.fromhex('02')


class TrainDetectionFCFailedReason:
    INCORRECT_COUNT = bytes.fromhex('01')
    TIMEOUT = bytes.fromhex('02')
    NOT_PERMITTED = bytes.fromhex('01')
    INTENTIONALLY_DELETED = bytes.fromhex('02')
    OUTGOING_DETECTED = bytes.fromhex('01')
    CANCELLED = bytes.fromhex('02')


class TrainDetectionPassingState:
    NOT_PASSED = bytes.fromhex('01')
    PASSED = bytes.fromhex('02')
    DISTURBED = bytes.fromhex('03')


class TrainDetectionPassingDirection:
    REFERENCE = bytes.fromhex('01')
    AGAINST_REFERENCE = bytes.fromhex('02')
    NOT_INDICATED = bytes.fromhex('03')


class EulynxTrainDetection(EulynxGeneric):
    protocol_type = bytes.fromhex('20')

    @classmethod
    def fc(cls, sender_id: str, receiver_id: str, mode: bytes) -> bytes:
        '''
        generate command to "Force section status to clear"

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the 
        :param mode: the FC mode

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0001')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += mode
        return message

    @classmethod
    def update_filling_level(cls, sender_id: str, receiver_id: str) -> bytes:
        '''
        generate command to request the filling level from the subsystem.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0002')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        return message

    @classmethod
    def cancel(cls, sender_id: str, receiver_id: str) -> bytes:
        '''
        generate command to force the subsystem to cancel the execution of FC-P and PC-P-A.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0008')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        return message

    @classmethod
    def drfc(cls, sender_id: str, receiver_id: str) -> bytes:
        '''
        generate command to force the subsystem to change its status to be able to be forced to clear.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0003')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        return message

    @classmethod
    def occupancy_status(
        cls,
        sender_id: str,
        receiver_id: str,
        occupancy_status: bytes,
        force_clear_ability: bytes,
        filling_level: int,
        pom_state: bytes,
        disturbance_state: bytes,
        change_trigger: bytes
    ) -> bytes:
        '''
        generate message to report the status of the subsystem

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param occupancy_status: the occupancy status of the TDS - see TrainDetectionOccupancyState class 
        :param force_clear_ability: the ability of the TDS to be forced to clear - see TrainDetectionForceClearAbility class
        :param filling_level: the filling level of the TDS - use negative value if not applicable
        :param pom_state: state of the power supply - see TrainDetectionPOMState class
        :param disturbance_state: the disturbance state of the TDS - see TrainDetectionDisturbanceState class
        :param change_trigger: the trigger for this message - see TrainDetectionChangeTrigger class

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0007')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += occupancy_status
        message += force_clear_ability
        if filling_level < 0:
            message += bytes.fromhex('FFFF')
        else:
            message += filling_level.to_bytes(2, 'big')
        message += pom_state
        message += disturbance_state
        message += change_trigger

        return message

    @classmethod
    def command_rejected(cls, sender_id: str, receiver_id: str, reason: bytes) -> bytes:
        '''
        generate message to inform requesting system about command rejection.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param reason: reason for the rejection - see TrainDetectionRejectionReason class

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0006')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += reason

        return message

    @classmethod
    def fcp_failed(cls, sender_id: str, receiver_id: str, reason: bytes) -> bytes:
        '''
        generate message to inform requesting system about failed FC-P execution.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param reason: reason for the rejection - see TrainDetectionFCFailedReason class

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0010')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += reason

        return message

    @classmethod
    def fcpa_failed(cls, sender_id: str, receiver_id: str, reason: bytes) -> bytes:
        '''
        generate message to inform requesting system about failed FC-P-A execution.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param reason: reason for the rejection - see TrainDetectionFCFailedReason class

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0011')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += reason

        return message

    @classmethod
    def additional_information(cls, sender_id: str, receiver_id: str, speed: bytes, diameter: bytes) -> bytes:
        '''
        generate message to report additional information.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param speed: measured vehicle speed in kmh, BCD encoded (2  bytes)
        :param diameter: the wheel diameter in mm, BCD encoded (2 bytes)

        Attention: according to Eu.SCI-TDS.PDI.[287,674,291,675] speed and wheel diameter
        shall be encoded in Binary Coded Decimal. It can however be defined by national requirements.

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0011')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        assert (len(speed) == 2)
        message += speed

        assert (len(diameter) == 2)
        message += diameter

        return message

    @classmethod
    def tdp_status(cls, sender_id: str, receiver_id: str, passing_state: bytes, passing_direction: bytes) -> bytes:
        '''
        generate message to report additional information.

        :param sender_id: Identifier of the sending instance of the command
        :param receiver_id: Identifier of the receiving instance of the
        :param passing_state: the state of passing - see TrainDetectionPassingState class
        :param passing_direction: the state of passing - see TrainDetectionPassingDirection class

        returns bytes 
        '''
        message = cls.protocol_type       # Protocol Type
        message += bytes.fromhex('0011')    # Message Type

        # sender Identifier
        sender_id = sender_id.encode('iso8859-1')
        message += sender_id + ((20 - len(sender_id)) * bytes.fromhex('5f'))

        # receiver Identifier
        receiver = receiver_id.encode('iso8859-1')
        message += receiver + ((20 - len(receiver)) * bytes.fromhex('5f'))

        message += passing_state
        message += passing_direction

        return message


class EulynxTrainDetectionParser(EulynxGenericParser):
    def __init__(self):
        self.fc_callbacks = []
        self.update_filling_level_callbacks = []
        self.cancel_callbacks = []
        self.drfc_callbacks = []
        self.occupancy_status_callbacks = []
        self.command_rejected_callbacks = []
        self.fcp_failed_callbacks = []
        self.fcpa_failed_callbacks = []
        self.additional_information_callbacks = []
        self.tdp_status_callbacks = []

    def parse_message(self, message: bytes) -> bool:
        '''
        parse a EULYNX message and call the registered callback functions if the message matches the supported types.

        :param message: EULYNX message as byte array

        returns True if the message could be parsed successfully, otherwise False
        '''
        if (len(message) > 42 and message[0].to_bytes(1,'big') == EulynxTrainDetection.protocol_type):
            sender = message[3:23].decode('iso8859-1').rstrip("_")
            receiver = message[23:43].decode('iso8859-1').rstrip("_")

            if (message[1:3] == bytes.fromhex('0001')):
                for func in self.fc_callbacks:
                    func[0](sender, receiver, message[43], func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0002')):
                for func in self.update_filling_level_callbacks:
                    func[0](sender, receiver, func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0008')):
                for func in self.cancel_callbacks:
                    func[0](sender, receiver, func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0003')):
                for func in self.drfc_callbacks:
                    func[0](sender, receiver, func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0007')):
                for func in self.occupancy_status_callbacks:
                    func[0](
                        sender,
                        receiver,
                        message[43],
                        message[44],
                        int.from_bytes(message[45:47], 'big'),
                        message[47],
                        message[48],
                        message[49],
                        func[1]
                    )
                return True
            elif (message[1:3] == bytes.fromhex('0006')):
                for func in self.command_rejected_callbacks:
                    func[0](sender, receiver, message[43], func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0010')):
                for func in self.fcp_failed_callbacks:
                    func[0](sender, receiver, message[43], func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0011')):
                for func in self.fcpa_failed_callbacks:
                    func[0](sender, receiver, message[43], func[1])
                return True
            elif (message[1:3] == bytes.fromhex('0012')):
                for func in self.additional_information_callbacks:
                    func[0](sender, receiver, message[43:45], message[45:], func[1])
                return True
            elif (message[1:3] == bytes.fromhex('000B')):
                for func in self.fcp_failed_callbacks:
                    func[0](sender, receiver, message[43], message[44], func[1])
                return True

        return False

    def register_fc_callback(self, function: Callable[[str, str, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "FC" EULYNX Command.

        :param function: Callable that accepts four parameters: sender id, receiver id, fc mode, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.fc_callbacks.append((function, params))

    def register_update_filling_level_callback(self, function: Callable[[str, str, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "Update Filling Level" EULYNX Command.

        :param function: Callable that accepts three parameters: sender id, receiver id, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.update_filling_level_callbacks.append((function, params))

    def register_cancel_callback(self, function: Callable[[str, str, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "Cancel" EULYNX Command.

        :param function: Callable that accepts three parameters: sender id, receiver id, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.cancel_callbacks.append((function, params))

    def register_drfc_callback(self, function: Callable[[str, str, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "DRFC" EULYNX Command.

        :param function: Callable that accepts three parameters: sender id, receiver id, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.drfc_callbacks.append((function, params))

    def register_occupancy_status_callback(self, function: Callable[[str, str, bytes, bytes, int, bytes, bytes, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "TVPS Occupancy Status" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, occupancy status, force clear ability, filling level, POM Status, Disturbance Status, Change Trigger
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.occupancy_status_callbacks.append((function, params))

    def regsiter_command_rejected_callback(self, function: Callable[[str, str, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "Command Rejected" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, rejection reason, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.command_rejected_callbacks.append((function, params))

    def register_fcp_failed_callback(self, function: Callable[[str, str, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "TVPS FC-P failed" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, failure reason, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.fcp_failed_callbacks.append((function, params))

    def register_fcpa_failed_callback(self, function: Callable[[str, str, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "TVPS FC-P-A failed" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, failure reason, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.fcpa_failed_callbacks.append((function, params))

    def regsiter_additional_information_callback(self, function: Callable[[str, str, bytes, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "Additional Information" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, speed, wheel diameter, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.additional_information_callbacks.append((function, params))

    def register_tdp_status_callback(self, function: Callable[[str, str, bytes, bytes, tuple], None], params: tuple) -> None:
        '''
        Register a callback function for the "TDP Status" EULYNX Message.

        :param function: Callable that accepts three parameters: sender id, receiver id, passing state, passing direction, params
        :param params: tuple of parameters passed to the callable

        returns None
        '''
        self.tdp_status_callbacks.append((function, params))
