from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqbuffer import RqCharBuffer
from communication.rqbuffer import RqCharBuffer1
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rqprimitives import RqGroup
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class Img2Tz:
    def __init__(self, port, buffer=RqCharBuffer1(), address=0xFFFFFFFF):
        # type: (Port, RqCharBuffer, int) -> Img2Tz
        self.port = port
        self.buffer = buffer
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqGroup(RqByte(0x02), RqByte(self.buffer.number())),
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
                "Can not generate characteristic from the finger image: {0}".format(
                    confirmation.as_str()
                )
            )
