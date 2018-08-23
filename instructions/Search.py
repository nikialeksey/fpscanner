from ConfirmationCode import ConfirmationCode
from InstructionException import InstructionException
from communication import RqSimple
from communication import RsCheckSum
from communication import RsSimple
from communication.port import Port
from communication.rqbuffer import RqCharBuffer
from communication.rqbuffer import RqCharBuffer1
from communication.rqpid import RqPidCommand
from communication.rqprimitives import RqByte
from communication.rqprimitives import RqGroup
from communication.rqprimitives import RqWord
from communication.rsprimitives import RsWord


class SearchResult:
    def __init__(self, content):
        # type: (bytearray) -> SearchResult
        self.content = content

    def code(self):
        return self.content[0]

    def number(self):
        return RsWord(self.content[1], self.content[2]).as_int()

    def score(self):
        return RsWord(self.content[3], self.content[4]).as_int()


class Search:
    def __init__(self, port, start, count, buffer=RqCharBuffer1(), address=0xFFFFFFFF):
        # type: (Port, int, int, RqCharBuffer, int) -> Search
        self.port = port
        self.rq = RqSimple(
            pid=RqPidCommand(),
            content=RqGroup(
                RqByte(0x04),
                RqByte(buffer.number()),
                RqWord(start),
                RqWord(count)
            ),
            address=address
        )
        self.rs = RsCheckSum(RsSimple(self.port))

    def execute(self):
        # type: () -> SearchResult
        self.rq.send_to(self.port)

        bytes = self.rs.bytes()
        confirmation = ConfirmationCode(bytes.content()[0])
        if bytes.content()[0] == 0x01:
            raise InstructionException(
                "Can not search finger: {0}".format(confirmation.as_str())
            )

        return SearchResult(bytes.content())
