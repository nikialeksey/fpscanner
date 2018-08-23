from CommunicationException import CommunicationException
from RsBytes import RsBytes
from RsPackage import RsPackage
from port import Port
from rsprimitives import RsWord


class RsSimple(RsPackage):
    def __init__(self, port):
        # type: (Port) -> RsSimple
        self.port = port

    def bytes(self):
        # type: () -> RsBytes
        response = self.port.bytes(
            2 +  # header
            4 +  # address
            1 +  # rqpid
            2  # length
        )

        if not response:
            raise CommunicationException("Seems that fingerprint scanner is not connected")

        last_index = len(response) - 1
        length = RsWord(response[last_index - 1], response[last_index]).as_int()

        response += self.port.bytes(length)

        return RsBytes(response)
