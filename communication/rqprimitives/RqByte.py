from RqBytes import RqBytes


class RqByte(RqBytes):
    def __init__(self, data):
        # type: (int) -> RqByte
        self.data = data

    def as_bytes(self):
        # type: () -> bytearray
        return bytearray([self.data & 0xFF])
