#!/usr/bin/python3

import datetime
import serial
import sys

assert len(sys.argv) == 3
filename = sys.argv[1]
channel = sys.argv[2]

def stop_acq(ser):
    ser.write(b'S')

def start_acq(ser, channel):
    if channel == 1:
        period = 10000
        resistor = 10
        ch = b'1'
    elif channel == 2:
        period = 5000
        resistor = 3.4
        ch = b'2'
    elif channel == 3:
        period = 5000
        resistor = 0.1
        ch = b'3'
    else:
        raise Exception('Unknown channel')
    ser.write(ch)
    return (period, resistor)


with serial.Serial('/dev/ttyACM0', 115200, xonxoff=0, timeout=None) as ser:
    stop_acq(ser)
    with open(filename, 'wb') as lf:
        (period, resistor) = start_acq(ser, int(channel))
        lf.write(str(datetime.datetime.now()).encode('utf-8'))
        lf.write('\n'.encode('utf-8'))
        lf.write(str(period).encode('utf-8'))
        lf.write('\n'.encode('utf-8'))
        lf.write(str(resistor).encode('utf-8'))
        lf.write('\n'.encode('utf-8'))
        count = 0
        while True:
            b = ser.read(50)
            lf.write(b)
            count += 1
            if count == 10:
                print('.')
                count = 0

