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
import struct

from serial import Serial

from Port import Port


class SerialPort(Port):

    def __init__(self, serial):
        # type: (Serial) -> SerialPort
        self.serial = serial

    def __enter__(self):
        if self.serial.isOpen():
            self.serial.close()
        self.serial.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serial.close()

    def bytes(self, length):
        # type: (int) -> bytearray
        return bytearray(
            map(
                lambda x: struct.unpack('@B', x)[0],
                self.serial.read(length)
            )
        )

    def send(self, bytes):
        # type: (bytearray) -> None
        self.serial.write(bytes)
