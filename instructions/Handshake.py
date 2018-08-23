from ConfirmationCode import ConfirmationCode
from InstructionException import InstructionException
from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte


class Handshake:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> Handshake
        self.port = port
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x17),
            address=address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> None
        self.rq.send_to(self.port)
        bytes = self.rs.bytes()

        confirmation = ConfirmationCode(bytes.content()[0])
        if not confirmation.is_success():
            raise InstructionException("Can not handshake: {0}".format(confirmation.as_str()))
