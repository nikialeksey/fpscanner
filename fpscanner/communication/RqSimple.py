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
from RqPackage import RqPackage
from port import Port
from rqpid import RqPid
from rqprimitives import RqByte
from rqprimitives import RqBytes
from rqprimitives import RqDword
from rqprimitives import RqWord


class RqSimple(RqPackage):

    def __init__(self, pid, port, header=0xEF01, address=0xFFFFFFFF):
        # type: (RqPid, Port, int, int) -> RqSimple
        self.header = header
        self.address = address
        self.pid = pid
        self.port = port

    def send(self, content):
        # type: (RqBytes) -> None
        content = content.as_bytes()
        length = len(content) + 2

        request = RqWord(self.header).as_bytes() + \
                  RqDword(self.address).as_bytes() + \
                  RqByte(self.pid.as_byte()).as_bytes() + \
                  RqWord(length).as_bytes()

        checksum = request[6] + request[7] + request[8]
        # content
        for byte in content:
            request.append(byte)
            checksum += byte

        # checksum
        request += RqWord(checksum).as_bytes()

        self.port.send(request)
