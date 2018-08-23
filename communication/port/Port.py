import abc


class Port:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def bytes(self, length):
        # type: (int) -> bytearray
        """
        Read specified length bytes.

        :param length: length of bytes to read
        :return: bytes array
        """

    @abc.abstractmethod
    def send(self, bytes):
        # type: (bytearray) -> None
        """
        Write bytes.

        :param bytes: byte array
        """
