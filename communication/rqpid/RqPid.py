import abc


class RqPid:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def as_byte(self):
        # type: () -> int
        """
        :return: rqpid value
        """
