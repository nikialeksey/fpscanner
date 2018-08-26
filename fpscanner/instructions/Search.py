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
from ConfirmationCode import ConfirmationCode
from InstructionException import InstructionException
from ..communication import RqPackage
from ..communication import RsPackage
from ..communication.rqbuffer import RqCharBuffer
from ..communication.rqbuffer import RqCharBuffer1
from ..communication.rqprimitives import RqByte
from ..communication.rqprimitives import RqGroup
from ..communication.rqprimitives import RqWord
from ..communication.rsprimitives import RsWord


class SearchResult:
    def __init__(self, content):
        # type: (bytearray) -> SearchResult
        self.content = content

    def code(self):
        return self.content[0]

    def number(self):
        return RsWord(self.content[1], self.content[2]).as_int()

    def score(self):
        return RsWord(self.content[3], self.content[4]).as_int()


class Search:
    def __init__(self, rq, rs, start, count, buffer=RqCharBuffer1()):
        # type: (RqPackage, RsPackage, int, int, RqCharBuffer) -> Search
        self.rq = rq
        self.rs = rs
        self.content = RqGroup(
            RqByte(0x04),
            RqByte(buffer.number()),
            RqWord(start),
            RqWord(count)
        )

    def execute(self):
        # type: () -> SearchResult
        self.rq.send(self.content)

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if bytes.content()[0] == 0x01:
            raise InstructionException(
                "Can not search finger: {0}".format(confirmation.as_str())
            )

        return SearchResult(bytes.content())
