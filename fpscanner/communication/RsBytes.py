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
from CommunicationException import CommunicationException
from rsprimitives import RsDword
from rsprimitives import RsWord


class RsBytes:
    def __init__(self, raw):
        # type: (bytearray) -> RsBytes
        self.raw = raw

    def header(self):
        # type: () -> int
        length = len(self.raw)
        if length < 2:
            raise CommunicationException(
                "Can not read header, because package length is not valid. Expected >= 2, but real {0}".format(length)
            )
        return RsWord(self.raw[0], self.raw[1]).as_int()

    def address(self):
        # type: () -> int
        length = len(self.raw)
        if length < 6:
            raise CommunicationException(
                "Can not read address, because package length is not valid. Expected >= 6, but real {0}".format(length)
            )
        return RsDword(self.raw[2], self.raw[3], self.raw[4], self.raw[5]).as_int()

    def pid(self):
        # type: () -> int
        length = len(self.raw)
        if length < 7:
            raise CommunicationException(
                "Can not read rqpid, because package length is not valid. Expected >= 7, but real {0}".format(length)
            )
        return self.raw[6]

    def length(self):
        # type: () -> int
        length = len(self.raw)
        if length < 9:
            raise CommunicationException(
                "Can not read length, because package length is not valid. Expected >= 9, but real {0}".format(length)
            )
        return RsWord(self.raw[7], self.raw[8]).as_int()

    def content(self):
        # type: () -> bytearray
        length = self.length()  # package content length + checksum

        real_length = len(self.raw)
        expected_length = 9 + length
        if real_length != expected_length:
            raise CommunicationException(
                "Can not read content, because package length is not valid. Expected {0}, but real {1}".format(
                    expected_length, real_length
                )
            )

        content = []
        for i in range(9, expected_length - 2):
            content.append(self.raw[i])

        return bytearray(content)

    def checksum(self):
        # type: () -> int
        length = self.length()  # package content length + checksum

        real_length = len(self.raw)
        expected_length = 9 + length
        if real_length != expected_length:
            raise CommunicationException(
                "Can not read checksum, because package length is not valid. Expected {0}, but real {1}".format(
                    expected_length, real_length
                )
            )
        return RsWord(self.raw[real_length - 2], self.raw[real_length - 1]).as_int()

    def __str__(self):
        return "Header: {0}, address: {1}, rqpid: {2}, length: {3}, content: {4}, checksum: {5}".format(
            self.header(),
            self.address(),
            self.pid(),
            self.length(),
            self.content(),
            self.checksum()
        )
