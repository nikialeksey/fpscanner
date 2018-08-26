from Port import Port


class LoggablePort(Port):

    def __init__(self, origin):
        # type: (Port) -> LoggablePort
        self.origin = origin

    def __enter__(self):
        self.origin.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.origin.__exit__(exc_type, exc_val, exc_tb)

    def bytes(self, length):
        # type: (int) -> bytearray
        result = self.origin.bytes(length)
        print(map(lambda x: int(x), result))
        return result

    def send(self, bytes):
        # type: (bytearray) -> None
        print(map(lambda x: int(x), bytes))
        self.origin.send(bytes)
