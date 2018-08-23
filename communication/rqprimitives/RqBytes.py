import abc


class RqBytes:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def as_bytes(self):
        # type: () -> bytearray
        """
        :return: bytes list
        """
