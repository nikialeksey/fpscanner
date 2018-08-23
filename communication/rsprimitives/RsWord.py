class RsWord:
    def __init__(self, high, low):
        # type: (int, int) -> RsWord
        self.high = high
        self.low = low

    def as_int(self):
        # type: () -> int
        return (self.high << 8) | self.low
