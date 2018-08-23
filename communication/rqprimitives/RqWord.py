from RqBytes import RqBytes


class RqWord(RqBytes):
    def __init__(self, data):
        # type: (int) -> RqWord
        self.data = data

    def as_bytes(self):
        # type: () -> bytearray
        return bytearray([(self.data >> 8) & 0xFF, self.data & 0xFF])
