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
