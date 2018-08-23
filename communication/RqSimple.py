from RqPackage import RqPackage
from port import Port
from rqpid import RqPid
from rqprimitives import RqByte
from rqprimitives import RqBytes
from rqprimitives import RqDword
from rqprimitives import RqWord


class RqSimple(RqPackage):

    def __init__(self, pid, content, header=0xEF01, address=0xFFFFFFFF):
        # type: (RqPid, RqBytes, int, int) -> RqSimple
        self.header = header
        self.address = address
        self.pid = pid
        self.content = content

    def send_to(self, port):
        # type: (Port) -> None
        content = self.content.as_bytes()
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

        port.send(request)
