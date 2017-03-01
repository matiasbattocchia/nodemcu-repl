import os
import sys
import serial
import argparse
import re

from time import sleep
from threading import Thread

from prompt_toolkit import prompt
from pygments.lexers import LuaLexer
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory

history = FileHistory('.nodemcu-repl_history')

loop_condition = True

NO_ECHO = 'uart.setup(0, 115200, 8, uart.PARITY_NONE, uart.STOPBITS_1, 0)'


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


def do_exit():
    global loop_condition
    loop_condition = False


def do_copy(command):
    source = command.split(' ')[-1]
    destination = os.path.basename(source)

    try:
        file = open(source, 'r')
        cmd = 'file.open("%s", "w")' % destination
        send(cmd)

        for line in file:
          cmd = 'file.writeline([==[%s]==])' % line.strip()
          send(cmd)

        file.close()
        send('file.close()')
        send('print()')

    except:
        sys.stdout.write('Error: Could not open input file "%s".\n' % source)
        sys.stdout.write('> ')
        sys.stdout.flush()


def do_list():
    cmd = 'for k,v in pairs(file.list()) do print(string.format("%4d %s", v, k)) end'
    send(cmd)


def user_loop():
    while loop_condition:

        try:
            command = prompt('', lexer=PygmentsLexer(LuaLexer), history=history)

            # Intercept commands starting with a dot.
            if re.match('\\.', command):
                command = command.lstrip('.')

                if   re.match('e|q', command):     do_exit()
                elif re.match('h', command):       do_help()
                elif re.match('cp|copy', command): do_copy(command)
                elif re.match('ls|list', command): do_list()
                #elif re.match('rm|remove', command): do_remove(command)
                else:
                    sys.stdout.write('Error: Command not understood.\n')
                    sys.stdout.write('> ')
                    sys.stdout.flush()

            else:
                send(command)

        except KeyboardInterrupt:
            do_exit()


def node_loop():
    while loop_condition:
        response = ser.read()
        sys.stdout.write(response.decode('utf-8'))
        sys.stdout.flush()

    ser.close()


def send(command):
    command = command + '\n'
    ser.write(command.encode('utf-8'))
    sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NodeMCU serial client')

    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', \
                        help='Device name, default /dev/ttyUSB0')

    parser.add_argument('-b', '--baud', default=115200, \
                        help='Baudrate, default 115200')

    args = parser.parse_args()

    ser = serial.Serial(args.port, args.baud)
    ser.timeout = 1

    sys.stdout.write('NodeMCU REPL\n')
    sys.stdout.write('Enter ".help" for usage hints.\n')
    sys.stdout.write('> ')
    sys.stdout.flush()

    send(';') # This closes any previous unfinished chunk
    send(NO_ECHO) # It is nicer without NodeMCU echo
    ser.reset_input_buffer() # Cleans the clutter generated earlier

    Thread(target=node_loop).start()
    user_loop()
