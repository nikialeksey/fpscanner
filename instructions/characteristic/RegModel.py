from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class RegModel:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> RegModel
        self.port = port
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x05),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> None
        self.rq.send_to(self.port)

        bytes = self.rs.bytes()

        content = bytes.content()
        confirmation = ConfirmationCode(content[0])
        if not confirmation.is_success():
            raise InstructionException("Can not generate a template: {0}".format(confirmation.as_str()))
