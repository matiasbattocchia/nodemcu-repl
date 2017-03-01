import os
import sys
import serial
import argparse
import re

from threading import Thread
from queue import Queue
from time import sleep

from prompt_toolkit import prompt
from pygments.lexers import LuaLexer
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory

history = FileHistory('nodemcu-repl_history')

queue = Queue()
loop_condition = True

NO_ECHO = 'uart.setup(0, 115200, 8, uart.PARITY_NONE, uart.STOPBITS_1, 0)'
queue.put(NO_ECHO)

def do_help():
    help = \
""".copy FILE\t Upload local FILE to device
.exit\t\t Exit this program
.list\t\t List files in device
.quit\t\t Quit this program
.remove FILE\t Remove FILE from device\n"""

    sys.stdout.write(help)
    sys.stdout.write('> ')
    sys.stdout.flush()


def do_copy(command):
    source = command.split(' ')[-1]
    destination = os.path.basename(source)

    try:
        file = open(source, 'rt')
        cmd = 'file.open("%s", "w")' % destination
        queue.put(cmd)

        for line in file:
          cmd = 'file.writeline([==[%s]==])' % line.strip()
          queue.put(cmd)

        file.close()
        queue.put('file.close()')
        queue.put('print()')

    except:
        sys.stdout.write('Error: Could not open input file "%s".\n' % source)
        sys.stdout.write('> ')
        sys.stdout.flush()


def do_list():
    cmd = 'for k,v in pairs(file.list()) do print(string.format("%4d %s", v, k)) end'
    queue.put(cmd)


def user_loop(queue):
    global loop_condition

    sys.stdout.write('NodeMCU REPL\n')
    sys.stdout.write('Enter ".help" for usage hints.\n')

    while loop_condition:

        command = prompt('', lexer=PygmentsLexer(LuaLexer), history=history)

        # Intercept commands starting with a dot.
        if re.match('\\.', command):
            command = command.lstrip('.')

            if   re.match('e|q', command):     loop_condition = False
            elif re.match('h', command):       do_help()
            elif re.match('cp|copy', command): do_copy(command)
            elif re.match('ls|list', command): do_list()
            #elif re.match('rm|remove', command): do_remove(command)
            else:
                sys.stdout.write('Error: Command not understood.\n')
                sys.stdout.write('> ')
                sys.stdout.flush()

        else:
          queue.put(command)


def node_loop(queue):
    while loop_condition:

        if ser.in_waiting > 0:
            response = ser.read(ser.in_waiting).decode('utf-8')
            sys.stdout.write(response)
            sys.stdout.flush()

        if not queue.empty():
            command = queue.get()

            command = command + '\n'
            # command = 'print(' + command + ')\n'

            ser.write(command.encode('utf-8'))

        sleep(0.3)

    ser.flush()
    ser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NodeMCU serial client')

    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', \
                        help='Device name, default /dev/ttyUSB0')

    parser.add_argument('-b', '--baud', default=115200, \
                        help='Baudrate, default 115200')

    args = parser.parse_args()

    ser = serial.Serial(args.port, args.baud)
    ser.timeout = 3
    ser.interCharTimeout = 3

    Thread(target=node_loop, args=(queue,)).start()
    Thread(target=user_loop, args=(queue,)).start()
