from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rsprimitives import RsWord
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class Match:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> Match
        self.port = port
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x03),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def score(self):
        # type: () -> int
        self.rq.send_to(self.port)
        bytes = self.rs.bytes()
        content = bytes.content()
        confirmation = ConfirmationCode(content[0])
        if confirmation.is_success():
            return RsWord(content[1], content[2]).as_int()
        else:
            raise InstructionException("Can not match: {0}".format(confirmation.as_str()))
