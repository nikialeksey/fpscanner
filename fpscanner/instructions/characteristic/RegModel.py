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
from ...communication import RqSimple
from ...communication import RsCheckSum
from ...communication import RsSimple
from ...communication.port import Port
from ...communication.rqpid import RqPidCommand
from ...communication.rqprimitives import RqByte
from ...instructions.ConfirmationCode import ConfirmationCode
from ...instructions.InstructionException import InstructionException


class RegModel:
    def __init__(self, port, address=0xFFFFFFFF):
        # type: (Port, int) -> RegModel
        self.port = port
        self.address = address
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqByte(0x05),
            address=self.address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> None
        self.rq.send_to(self.port)

        bytes = self.rs.bytes()

        content = bytes.content()
        confirmation = ConfirmationCode(content[0])
        if not confirmation.is_success():
            raise InstructionException("Can not generate a template: {0}".format(confirmation.as_str()))
