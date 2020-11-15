import unittest
from unittest import mock

from py328 import Arduino


class FakePort:
    def __init__(self, device, manufacturer):
        self.device = device
        self.manufacturer = manufacturer


class ArduinoConnectionTestCase(unittest.TestCase):

    @mock.patch('serial.Serial')
    @mock.patch('serial.tools.list_ports.comports')
    def test_arduino_connected(self, mock_comports, mock_serial):
        fake_port = FakePort(device='/foo/bar', manufacturer='Arduino super')
        mock_comports.return_value = [fake_port]

        board = Arduino()

        self.assertIsNotNone(board.serial_port)

    @mock.patch('serial.tools.list_ports.comports')
    def test_arduino_not_connected_no_ports(self, mock_comports):
        mock_comports.return_value = []

        board = Arduino()

        self.assertIsNone(board.serial_port)

    @mock.patch('serial.tools.list_ports.comports')
    def test_arduino_not_connected_no_arduino_device(self, mock_comports):
        fake_port = FakePort(device='/foo/bar', manufacturer='Duino')
        mock_comports.return_value = [fake_port]

        board = Arduino()

        self.assertIsNone(board.serial_port)
