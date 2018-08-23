from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqbuffer import RqCharBuffer
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rqprimitives import RqGroup
from communication.rqprimitives import RqWord
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class Store:
    def __init__(self, port, buffer, number, address=0xFFFFFFFF):
        # type: (Port, RqCharBuffer, int, int) -> Store
        self.port = port
        self.buffer = buffer
        self.number = number
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqGroup(RqByte(0x06), RqByte(self.buffer.number()), RqWord(self.number)),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> None
        self.rq.send_to(self.port)

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if not confirmation.is_success():
            raise InstructionException(
                "Can not store template: {0}".format(
                    confirmation.as_str()
                )
            )
