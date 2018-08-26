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
from ...communication import RsPackage
from ...communication.rqbuffer import RqCharBuffer
from ...communication.rqbuffer import RqCharBuffer1
from ...communication.rqprimitives import RqByte
from ...communication.rqprimitives import RqGroup
from ...instructions.ConfirmationCode import ConfirmationCode
from ...instructions.InstructionException import InstructionException


class Img2Tz:
    def __init__(self, rq, rs, buffer=RqCharBuffer1()):
        # type: (RqPackage, RsPackage, RqCharBuffer) -> Img2Tz
        self.buffer = buffer
        self.rq = rq
        self.rs = rs

    def execute(self):
        # type: () -> None
        self.rq.send(RqGroup(RqByte(0x02), RqByte(self.buffer.number())))

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if not confirmation.is_success():
            raise InstructionException(
                "Can not generate characteristic from the finger image: {0}".format(
                    confirmation.as_str()
                )
            )
