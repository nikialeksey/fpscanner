from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from instructions.ConfirmationCode import ConfirmationCode


class GenImg:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> GenImg
        self.port = port
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x01),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> bool
        self.rq.send_to(self.port)
        bytes = self.rs.bytes()
        return ConfirmationCode(bytes.content()[0]).is_success()
