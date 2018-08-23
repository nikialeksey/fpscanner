import struct

from serial import Serial

from Port import Port


class SerialPort(Port):

    def __init__(self, serial):
        # type: (Serial) -> SerialPort
        self.serial = serial

    def __enter__(self):
        if self.serial.isOpen():
            self.serial.close()
        self.serial.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serial.close()

    def bytes(self, length):
        # type: (int) -> bytearray
        return bytearray(
            map(
                lambda x: struct.unpack('@B', x)[0],
                self.serial.read(length)
            )
        )

    def send(self, bytes):
        # type: (bytearray) -> None
        self.serial.write(bytes)
