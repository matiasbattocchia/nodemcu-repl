import sys
import serial
import time

from threading import Thread
from queue import Queue

PORT = '/dev/ttyUSB0'
BAUD = 115200
ser = serial.Serial(PORT, BAUD)
ser.timeout = 3
ser.interCharTimeout = 3

command_queue = Queue()

NO_ECHO = 'uart.setup(0, 115200, 8, uart.PARITY_NONE, uart.STOPBITS_1, 0)'
command_queue.put(NO_ECHO)

def user_loop(command_queue):
    sys.stdout.write('> ')

    while True:

        command = sys.stdin.readline().rstrip()
        command_queue.put(command)

        if command == 'EXIT': break


def node_loop(command_queue):
    while True:
        if ser.inWaiting() > 0:
            response = ser.read(ser.inWaiting())
            sys.stdout.write(response.decode('utf-8'))

        if not command_queue.empty():
            command = command_queue.get()

            if command == 'EXIT': break

            command = 'print(' + command + ')\n'

            ser.write(command.encode('utf-8'))

        time.sleep(0.3)

    ser.flush()
    ser.close()


if __name__ == "__main__":
    Thread(target=node_loop, args=(command_queue,)).start()
    Thread(target=user_loop, args=(command_queue,)).start()
