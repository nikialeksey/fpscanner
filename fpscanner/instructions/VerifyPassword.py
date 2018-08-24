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
from ..communication import RqSimple
from ..communication import RsCheckSum
from ..communication import RsSimple
from ..communication.port import Port
from ..communication.rqpid import RqPidCommand
from ..communication.rqprimitives import RqByte
from ..communication.rqprimitives import RqDword
from ..communication.rqprimitives import RqGroup


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
