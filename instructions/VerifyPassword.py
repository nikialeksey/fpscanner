from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rqprimitives import RqDword
from communication.rqprimitives import RqGroup


class VerifyPassword:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> VerifyPassword
        self.port = port
        self.address = address

    def execute(self):
        # type: () -> bool
        RqSimple(
            pid=RqPidCommand(),
            content=RqGroup(RqByte(0x13), RqDword(0)),
            address=self.address
        ).send_to(self.port)

        bytes = RsCheckSum(RsSimple(self.port)).bytes()
        return bytes.content()[0] == 0
