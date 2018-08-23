from RqBytes import RqBytes


class RqDword(RqBytes):
    def __init__(self, data):
        # type: (int) -> RqDword
        self.data = data

    def as_bytes(self):
        # type: () -> bytearray
        return bytearray([
            (self.data >> 24) & 0xFF,
            (self.data >> 16) & 0xFF,
            (self.data >> 8) & 0xFF,
            self.data & 0xFF
        ])
