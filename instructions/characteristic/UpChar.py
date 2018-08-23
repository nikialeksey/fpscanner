from communication import RqSimple
from communication import RsCheckSum
from communication import RsDataPacket
from communication import RsSimple
from communication.port import Port
from communication.rqbuffer import RqCharBuffer
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rqprimitives import RqGroup
from instructions.ConfirmationCode import ConfirmationCode
from instructions.InstructionException import InstructionException


class UpChar:
    def __init__(self, port, buffer, address=0xFFFFFFFF):
        # type: (Port, RqCharBuffer, int) -> UpChar
        self.port = port
        self.buffer = buffer
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqGroup(RqByte(0x08), RqByte(self.buffer.number())),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def characteristic(self):
        # type: () -> list[int]
        self.rq.send_to(self.port)

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if not confirmation.is_success():
            raise InstructionException(
                "Can not upload characteristic from buffer: {0}".format(confirmation.as_str())
            )

        characteristic = []
        for list in RsDataPacket(self.port).content():
            characteristic += list
        return characteristic
