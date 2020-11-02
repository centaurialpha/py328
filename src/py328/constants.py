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
import enum

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


class PinMode(enum.Flag):
    UNAVAILABLE = -0x1
    INPUT = 0x0
    OUTPUT = 0x1
    ANALOG = 0x2


class PinValue(enum.Flag):
    LOW = 0x0
    HIGH = 0x1


DIGITAL_PIN_COUNT = 14
ANALOG_PIN_COUNT = 6
UNAVAILABLE_DIGITAL_PINS = (0, 1)  # Rx, Tx
EXTERNAL_INTERRUPTS_PINS = (2, 3)
PWM_PINS = (3, 5, 6, 9, 11)
