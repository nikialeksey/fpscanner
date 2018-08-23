from RqBytes import RqBytes


class RqGroup(RqBytes):
    def __init__(self, *rq_bytes):
        # type: (list[RqBytes]) -> RqGroup
        self.rq_bytes = rq_bytes

    def as_bytes(self):
        # type: () -> bytearray
        return reduce(
            lambda acc, bytes: acc + bytes.as_bytes(),
            self.rq_bytes,
            bytearray()
        )
