import abc


class RqCharBuffer:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def number(self):
        # type: () -> int
        """
        :return: number of characteristic buffer
        """
