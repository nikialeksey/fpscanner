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
from RsBytes import RsBytes
from RsPackage import RsPackage


class RsCheckHeader(RsPackage):

    def __init__(self, package, expected=0xEF01):
        # type: (RsPackage, int) -> RsCheckHeader
        self.origin = package
        self.expected = expected

    def bytes(self):
        # type: () -> RsBytes
        bytes = self.origin.bytes()

        real = bytes.header()

        if self.expected != real:
            raise CommunicationException("Header does not valid. Expected {0}, was {1}".format(self.expected, real))

        return bytes
