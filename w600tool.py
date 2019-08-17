#!/usr/bin/env python3

import serial
import os
import sys
import time
import struct
import argparse

import pyprind
from xmodem import XMODEM1k

CMD_SET_BAUD = 0x31
CMD_ERASE    = 0x32 # ROM boot only
CMD_SET_SEC  = 0x33 # ROM boot only
CMD_GET_SEC  = 0x34 # ROM boot only
CMD_SET_GAIN = 0x35
CMD_GET_GAIN = 0x36
CMD_SET_MAC  = 0x37
CMD_GET_MAC  = 0x38
CMD_GET_QFID = 0x3c # ROM boot only

# CRC-16/CCITT-FALSE
def crc16(data : bytearray):
    crc = 0xFFFF
    for i in range(0, len(data)):
        crc ^= data[i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF

def putc(c):
    sys.stdout.write(c)
    sys.stdout.flush()

def error_exit(msg):
    print('Error:', msg)
    sys.exit(1)

ser = None

def deviceWaitBoot(timeout = 3):
    ser.timeout = 0.01
    ser.flushInput()
    started = time.time()
    buff = b''
    while time.time() - started < timeout:
        ser.write(b'\x1B')
        buff = buff + ser.read(1)
        buff = buff[-16:]            # Remember last 16 chars
        if buff.endswith(b'CCCC'):
            return True
    return False

def sendCommand(cmd):
    cmd = struct.pack('<BHH', 0x21, len(cmd)+2, crc16(cmd)) + cmd
    ser.flushInput()
    ser.write(cmd)
    ser.flush()
    #print('<<< ', cmd.hex())

def deviceSetBaud(baud):
    sendCommand(struct.pack('<II', CMD_SET_BAUD, baud))
    ser.close()
    ser.baudrate = baud
    ser.open()
    return deviceWaitBoot()

def deviceErase():
    ser.timeout = 1
    sendCommand(struct.pack('<I', CMD_ERASE))

def deviceSetMAC(mac):
    ser.timeout = 1
    sendCommand(struct.pack('<I', CMD_SET_MAC) + mac)

def deviceGetMAC():
    ser.timeout = 1
    sendCommand(struct.pack('<I', CMD_GET_MAC))
    result = ser.read_until(b'\n')
    result = result.decode('ascii').upper().strip()
    if result.startswith('MAC:'):
        return result[4:]
    return None

def deviceGetFlashID():
    ser.timeout = 1
    sendCommand(struct.pack('<I', CMD_GET_QFID))
    result = ser.read_until(b'\n')
    result = result.decode('ascii').upper().strip()
    if result.startswith('FID:'):
        return result[4:]
    return None

def deviceUploadFile(fn):
    ser.timeout = 1
    statinfo_bin = os.stat(fn)
    bar = pyprind.ProgBar(statinfo_bin.st_size//1024)

    def ser_write(data, timeout=1):
        bar.update()
        return ser.write(data)

    def ser_read(size, timeout=1):
        return ser.read(size)

    stream = open(fn, 'rb+')
    time.sleep(0.2)
    modem = XMODEM1k(ser_read, ser_write)
    ser.flushInput()
    if modem.send(stream):
        time.sleep(1)
        reply = ser.read_until(b'run user code...')
        reply = reply.decode('ascii').strip()
        return reply

    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',  default="/dev/ttyUSB0")
    parser.add_argument('--get-mac',     action="store_true")
    parser.add_argument('--set-mac')
    parser.add_argument('-e', '--erase', action="store_true")
    parser.add_argument('-u', '--upload')
    parser.add_argument('--upload-speed', default=1000000, type=int)
    args = parser.parse_args()

    ser = serial.Serial(args.port, 115200, timeout=1)

    if not deviceWaitBoot():
        print('Reset board to enter bootloader...')
        if not deviceWaitBoot(15):
            error_exit('Bootloader not detected')

    if args.set_mac:
        mac = args.set_mac.replace(':','').replace(' ','').upper()
        print('Setting MAC:', mac)
        deviceSetMAC(bytearray.fromhex(mac))

    if args.get_mac:
        mac = deviceGetMAC()
        print('MAC:', mac)

    if args.erase:
        if deviceGetFlashID() == None:
            error_exit('Secboot can\'t erase image, please enter ROM bootloader.')
        print('Erasing image...')
        deviceErase()

    if args.upload:
        if args.upload_speed != ser.baudrate:
            if deviceSetBaud(args.upload_speed):
                print('Switched speed to', ser.baudrate)
            else:
                error_exit('Cannot switch speed')

        print('Uploading', args.upload, '...')
        reply = deviceUploadFile(args.upload)
        print(reply)
