import abc

from RsBytes import RsBytes


class RsPackage:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def bytes(self):
        # type: () -> RsBytes
        """
        Retrieve bytes from response
        """
