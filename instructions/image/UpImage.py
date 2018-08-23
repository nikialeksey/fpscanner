from PIL import Image

from communication import RqSimple
from communication import RsCheckSum
from communication import RsDataPacket
from communication import RsSimple
from communication.port import Port
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from instructions.InstructionException import InstructionException


class UpImage:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> UpImage
        self.port = port
        self.address = address

    def execute(self):
        # type: () -> Image
        RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x0A),
            address=self.address
        ).send_to(self.port)

        bytes = RsCheckSum(RsSimple(self.port)).bytes()
        confirmation = bytes.content()[0]
        if confirmation != 0:
            raise InstructionException(
                "Can not execute UpImage, because there is not valid confirmation code: {0}".format(confirmation)
            )

        result = Image.new('L', (256, 288), 'white')
        pixels = result.load()

        content = RsDataPacket(self.port).content()
        y = 0
        for line in content:
            x = 0
            for c in line:
                pixels[x, y] = (c >> 4) * 17
                x = x + 1

                pixels[x, y] = (c & 0b00001111) * 17
                x = x + 1
            y += 1

        return result
