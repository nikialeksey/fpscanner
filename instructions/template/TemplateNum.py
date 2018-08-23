from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rsprimitives import RsWord
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class TemplateNum:

    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> TemplateNum
        self.port = port
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x1D),
            address=address
        )
        self.rs = RsCheckSum(RsSimple(port))

    def as_int(self):
        # type: () -> int
        self.rq.send_to(self.port)
        bytes = self.rs.bytes()

        content = bytes.content()
        confirmation = ConfirmationCode(content[0])
        if not confirmation.is_success():
            raise InstructionException("Incorrect confirmation code: {0}".format(confirmation.as_str()))

        return RsWord(content[1], content[2]).as_int()
