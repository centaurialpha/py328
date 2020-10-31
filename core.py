import enum
import serial
import time

WAIT_TO_INIT_BOARD = 5


class PINType(enum.IntEnum):
    ANALOG = 0
    DIGITAL = 1


class PINMode(enum.IntEnum):
    INPUT = 0
    OUTPUT = 1


class Arduino:

    def __init__(self, port='/dev/ttyACM0'):
        self.serial = serial.Serial(port, 9600, timeout=1)
        self._wait_non_blocking(WAIT_TO_INIT_BOARD)

    def _wait_non_blocking(self, wait_time):
        cont = time.time() + wait_time
        while time.time() < cont:
            time.sleep(0)

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.serial.write(data)

    def close(self):
        self.serial.close()


class Pin:

    def __init__(self, number, pin_type=PINType.DIGITAL, port=None):
        self._number: int = number
        self._type = pin_type
        self._port = port
        self._mode: PINMode = None
        self._value = None

    def __str__(self):
        return f'{self._type} PIN {self._number}'

    def write(self, value):
        pass

    def read(self):
        pass


class Port:

    def __init__(self, number):
        self._number = number

        self._pins = []
        for i in range(8):
            pin_nr = i + self._number * 8
            pin = Pin(
                number=pin_nr,
                pin_type=PINType.DIGITAL,
                port=self
            )
            self._pins.append(pin)

    def write(self):
        pass
