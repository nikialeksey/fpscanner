# MIT License
#
# Copyright (c) 2018 Alexey Nikitin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from PIL import Image

from ...communication import RqSimple
from ...communication import RsCheckSum
from ...communication import RsDataPacket
from ...communication import RsSimple
from ...communication.port import Port
from ...communication.rqpid import RqPidCommand
from ...communication.rqprimitives import RqByte
from ...instructions.InstructionException import InstructionException


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
