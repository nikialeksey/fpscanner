from CommunicationException import CommunicationException
from RsBytes import RsBytes
from RsPackage import RsPackage


class RsCheckSum(RsPackage):

    def __init__(self, package):
        # type: (RsPackage) -> RsCheckSum
        self.origin = package

    def bytes(self):
        # type: () -> RsBytes
        bytes = self.origin.bytes()

        expected = bytes.pid()

        length = bytes.length()
        expected += (length >> 8) + (length & 0xFF)

        for c in bytes.content():
            expected += c
        expected = expected & 0xFFFF

        real = bytes.checksum()

        if expected != real:
            raise CommunicationException("Checksum is invalid. Expected {0}, was {1}".format(expected, real))

        return bytes
