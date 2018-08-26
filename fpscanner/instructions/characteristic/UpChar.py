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
from ...communication import RqPackage
from ...communication import RsDataPacket
from ...communication import RsPackage
from ...communication.rqbuffer import RqCharBuffer
from ...communication.rqprimitives import RqByte
from ...communication.rqprimitives import RqGroup
from ...instructions.ConfirmationCode import ConfirmationCode
from ...instructions.InstructionException import InstructionException


class UpChar:
    def __init__(self, rq, rs, buffer):
        # type: (RqPackage, RsPackage, RqCharBuffer) -> UpChar
        self.buffer = buffer
        self.rq = rq
        self.rs = rs

    def characteristic(self):
        # type: () -> bytearray
        self.rq.send(RqGroup(RqByte(0x08), RqByte(self.buffer.number())))

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if not confirmation.is_success():
            raise InstructionException(
                "Can not upload characteristic from buffer: {0}".format(confirmation.as_str())
            )

        characteristic = bytearray([])
        for list in RsDataPacket(self.rs).content():
            characteristic += list
        return characteristic
