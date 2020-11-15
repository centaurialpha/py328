# Copyright - Gabriel Acosta <acostadariogabriel@gmail.com>
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
import warnings

import serial
import serial.tools.list_ports

from py328.constants import (
    SYSEX_START,
    SYSEX_END,
    SET_PIN_MODE,
    SET_DIGITAL_PIN_VALUE,
    UNAVAILABLE_DIGITAL_PINS,
)

r"""
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

**************************************************

DDR register: determinate if the PIN is INPUT or OUTPUT (read/write)
PORT register: HIGH or LOW (read/write)
PIN register: read PIN state configured as INPUT (read)
"""

__version__ = '0.1'


class Arduino:
    WAIT_TO_INIT_BOARD = 4

    def __init__(self, port=None, baud_rate=57600):
        self.serial_port = port
        self.baud_rate = baud_rate

        if port is None:
            try:
                self._find_arduino()
            except IOError as reason:
                print('> Error while find arduino device')
                print(f'    {reason}')
        else:
            self._connect_arduino()

        if self.serial_port is not None:
            print(f'> Arduino device compatible connected on {self.serial_port.name}')

    def _connect_arduino(self):
        pass

    def _find_arduino(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            raise IOError('No device connected on serial port')

        candidate_ports = [port for port in ports if 'Arduino' in port.manufacturer]
        if not candidate_ports:
            raise IOError('No Arduino connected on serial port')

        if len(candidate_ports) > 1:
            warnings.warn('More than one Arduino connected, will be use first')
        candidate_port = candidate_ports[0]

        self.serial_port = serial.Serial(candidate_port.device, baudrate=self.baud_rate)

    def _send_sysex(self, command):
        # Prepare sysex command
        cmd = (
            SYSEX_START,
            command,
            SYSEX_END
        )
        self.send_command(cmd)

    def send_command(self, command):
        if isinstance(command, tuple):
            command = bytes(command)
        self.serial_port.write(command)

    def going_down(self):
        if self.serial_port is not None:
            self.serial_port.close()

    def __del__(self):
        self.going_down()


class Pin:
    """Pin representation"""

    def __init__(self, number: int, board=None):
        if number in UNAVAILABLE_DIGITAL_PINS:
            raise IOError(f'Pin {number} not available')
        self._number = number
        self._mode = None
        self._value = None

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
    def mode(self, pin_mode):
        if self._board is None:
            raise RuntimeError("Board is not set")

        if self._mode != pin_mode:
            self._mode = pin_mode
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


class Port:
    """8 bit digital port representation"""

    def __init__(self):
        self.pins = []
