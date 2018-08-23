class RsDword:
    def __init__(self, byte3, byte2, byte1, byte0):
        # type: (int, int, int, int) -> RsDword
        self.byte3 = byte3
        self.byte2 = byte2
        self.byte1 = byte1
        self.byte0 = byte0

    def as_int(self):
        return (self.byte3 << 24) | (self.byte2 << 16) | (self.byte1 << 8) | self.byte0
