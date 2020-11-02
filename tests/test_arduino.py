import unittest
from unittest import mock

from py328 import Arduino


class ArduinoTestCase(unittest.TestCase):

    def setUp(self):
        self.board = Arduino()


