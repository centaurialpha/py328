# Copyright 2015-2020 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of PY328.
#
# PY328 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# PY328 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PY328; If not, see <http://www.gnu.org/licenses/>.
import enum
from typing import List

r"""
Just to remember me - gabox
                                   +-----+
      +----[PWR]-------------------| USB |--+
      |                            +-----+  |
      |         GND/RST2  [ ][ ]            |
      |       MOSI2/SCK2  [ ][ ]  A5/SCL[ ] |   C5
      |          5V/MISO2 [ ][ ]  A4/SDA[ ] |   C4
      |                             AREF[ ] |
      |                              GND[ ] |
      | [ ]N/C                    SCK/13[ ] |   B5
      | [ ]IOREF                 MISO/12[ ] |   .
      | [ ]RST                   MOSI/11[ ]~|   .
      | [ ]3V3    +---+               10[ ]~|   .
      | [ ]5v     | A |                9[ ]~|   .
      | [ ]GND   -| R |-               8[ ] |   B0
      | [ ]GND   -| D |-                    |
      | [ ]Vin   -| U |-               7[ ] |   D7
      |          -| I |-               6[ ]~|   .
      | [ ]A0    -| N |-               5[ ]~|   .
      | [ ]A1    -| O |-               4[ ] |   .
      | [ ]A2     +---+           INT1/3[ ]~|   .
      | [ ]A3                     INT0/2[ ] |   .
      | [ ]A4/SDA  RST SCK MISO     TX>1[ ] |   .
      | [ ]A5/SCL  [ ] [ ] [ ]      RX<0[ ] |   D0
      |            [ ] [ ] [ ]              |
      |  UNO_R3    GND MOSI 5V  ____________/
       \_______________________/

       http://busyducks.com/ascii-art-arduinos

**************************************************

+-----+---------------+
|Port |   PINs        |
+-----+---------------+
|B    |  8-13         |
|C    |  0-5 (analog) |
|D    |  0-7          |
+-----+---------------+
"""

__version__ = '0.1'

import serial
import time

# Send data for a digital pin
DIGITAL_MESSAGE = 0x90
# Send data for a analog pin
ANALOG_MESSAGE = 0xE0
# Start/end System Exclusive message (sysex)
SYSEX_START = 0xF0
SYSEX_END = 0xF7
# Set pin mode
SET_PIN_MODE = 0xF4
# Set digital pin value
SET_DIGITAL_PIN_VALUE = 0xF5
# Report version of firmware
REPORT_VERSION = 0xF9
# Report the firmware name
REPORT_FIRMWARE = 0x79


class PinMode(enum.IntEnum):
    INPUT = 0
    OUTPUT = 1
    ANALOG = 2


class PinValue(enum.IntEnum):
    LOW = 0
    HIGH = 1


DIGITAL_PIN_COUNT = 14
ANALOG_PIN_COUNT = 6


class Arduino:
    WAIT_TO_INIT_BOARD = 4

    def __init__(self, port=None):
        self._serial_port = serial.Serial(port, 57600, timeout=1)

        self.pins: List[Pin] = [
            Pin(pin_number).set_board(self)
            for pin_number in range(DIGITAL_PIN_COUNT)
        ]
        self._firmware_version = None

        # TODO: find board automatically
        print('Wait to start board...')
        time.sleep(self.WAIT_TO_INIT_BOARD)
        print('Retrieving firmware version...')
        self._report_board_firmware()

    def _report_board_firmware(self):
        # Prepare sysex command
        cmd = (
            SYSEX_START,
            REPORT_FIRMWARE,
            SYSEX_END
        )
        self.send_command(cmd)
        data = list(self._serial_port.read_until(b'\xf7'))
        major, minor = data[2:4]
        name = ''.join([chr(i) for i in data[4:-1]])

        self._firmware_version = (major, minor, name)

    def send_command(self, command):
        if isinstance(command, tuple):
            command = bytes(command)
        self._serial_port.write(command)

    def set_pin_mode(self, pin: int, mode: PinMode):
        self.pins[pin].mode = mode

    def write_digital_pin(self, pin: int, value: PinValue):
        self.pins[pin].write(value)

    def delay_secs(self, secs: float):
        time.sleep(secs)

    def delay_ms(self, ms: float):
        time_ms = ms / 1000
        time.sleep(time_ms)

    def going_down(self):
        pass


class Pin:
    """Pin representation"""

    def __init__(self, number: int, *, mode: PinMode = None):
        self._number = number
        self._mode = mode
        self._value = None

        self._board = None

    def set_board(self, board):
        self._board = board

    @property
    def value(self) -> int:
        return self._value

    @property
    def number(self) -> int:
        return self._number

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        if self._board is None:
            raise RuntimeError("Board is not set")

        if self._mode != m:
            self._mode = m
            cmd = (SET_PIN_MODE, self._number, self._mode)
            self._board.send_command(cmd)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'PIN(n={self._number}, m={self._mode})'

    def write(self, value: int):
        if self._board is None:
            raise RuntimeError("Board is not set")

        if self._value != value:
            self._value = value
            cmd = (SET_DIGITAL_PIN_VALUE, self._number, self._value)
            self._board.send_command(cmd)
