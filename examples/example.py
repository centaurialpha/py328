import sys

from py328 import (
    Arduino,
    PinMode,
    PinValue
)

PIN = 13


def main(port):
    board = Arduino(port=port)
    board.set_pin_mode(PIN, PinMode.OUTPUT)

    while True:
        board.write_digital_pin(PIN, PinValue.HIGH)
        board.delay_ms(100)
        board.write_digital_pin(PIN, PinValue.LOW)
        board.delay_ms(100)


if __name__ == '__main__':
    port = sys.argv[1]
    main(port)
