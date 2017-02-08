import sys
import serial

PORT = '/dev/ttyUSB0'
BAUD = 115200
ser = serial.Serial(PORT, BAUD)
ser.timeout = 3
ser.interCharTimeout = 3

def writeln(data):
    ser.write(data.encode('utf-8'))

def read(length):
    return ser.read(length)

def close():
    ser.flush()
    ser.close()


def shell_loop():

    while True:
        # Display a command prompt
        sys.stdout.write('> ')

        # Read command input
        cmd = sys.stdin.readline()

        if cmd == "EXIT\n": break

        # Execute the command
        #writeln('print(' + cmd + ')')
        writeln(cmd)

        # Print the output
        sys.stdout.write(ser.readline().decode('utf-8'))

    close()

def main():
    shell_loop()

if __name__ == "__main__":
    main()
