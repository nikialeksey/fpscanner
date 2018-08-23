import abc

from port import Port


class RqPackage:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send_to(self, port):
        # type: (Port) -> None
        """
        Asynchronously send request package to serial port
        :param port: port for sending package
        :return: nothing
        """
