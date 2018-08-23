from RqPid import RqPid


class RqPidCommand(RqPid):
    def as_byte(self):
        # type: () -> int
        return 0x01
