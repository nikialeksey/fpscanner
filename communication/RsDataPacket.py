from RsCheckSum import RsCheckSum
from RsSimple import RsSimple
from port import Port


class RsDataPacket:
    def __init__(self, port):
        # type: (Port) -> RsDataPacket
        self.port = port

    def content(self):
        # type: () -> list[bytearray]
        content = []
        n = 0  # number of packets

        rs = RsCheckSum(RsSimple(self.port))
        bytes = rs.bytes()
        while bytes.pid() != 0x08:
            content.append(bytes.content())
            bytes = rs.bytes()
            n += 1
        content.append(bytes.content())

        return content
