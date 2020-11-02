import unittest
from unittest import mock

from py328.py328 import Pin, Arduino, PinMode
from py328.constants import UNAVAILABLE_DIGITAL_PINS


class PinTestCase(unittest.TestCase):

    def setUp(self):
        self.board = mock.Mock(spec=Arduino)

    def test_unavailable_pin(self):
        rx_tx_pins = [0, 1]
        unavailable_pins = rx_tx_pins
        for unavailable_pin in unavailable_pins:
            with self.subTest(pin=unavailable_pin):
                with self.assertRaises(IOError):
                    Pin(number=unavailable_pin)

    def _create_pin(self, number, mode):
        pin = Pin(number=number, board=self.board)
        pin.mode = mode

        self.assertEqual(pin.mode, mode)
        return pin

    def test_set_pin_mode(self):
        PIN_NUMBER = 4

        pin_4 = self._create_pin(PIN_NUMBER, PinMode.OUTPUT)

        cmd=(0xf4, PIN_NUMBER, PinMode.OUTPUT)
        self.board.send_command.assert_called_with(cmd)
