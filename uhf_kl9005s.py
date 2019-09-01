#!/usr/local/bin/python

# Author: Thorsten Bosbach 09/2019

import time
import sys
import serial
import usb
import binascii
import struct

def checksum(bytes):
    # first assumption ;-) sum + crc = 0x200, crc = 0x200 - sum
    sum = 0x0
    for i in bytes:
        sum += i
    #print ('     sum: {:02x}'.format(sum))
    sum_crc = sum
    i = 0
    while sum_crc > 0xf:
        sum_crc = sum_crc >> 4
        i += 1
    if ((sum_crc << (4*i)) < sum):
        sum_crc = (sum_crc+1) << (4*i)
    else:
        sum_crc = sum_crc << (4*i)
    #print ('     {:02x}'.format(sum_crc) + " " + str(i))
    sum_crc -= sum
    #print ('     0x200 - sum: {:02x}'.format(sum_crc))
    return sum_crc

def send(ser, bytes, adr=0xff):
    bytes.insert(0,struct.pack("B", len(bytes)+1))
    bytes.insert(0,adr)
    bytes.insert(0,0x0a)
    sum_crc = checksum(bytes)
    bytes.append(sum_crc)
    x = ser.write(bytes)
    #str(x)+
    print ("<: "+"".join('{:02x} '.format(x) for x in bytes))

def receive(ser):
    bytes0 = ser.read(3)
    if (len(bytes0) > 0):
        bytes1 = ser.read(ord(bytes0[2]))
        bytes0 += bytes1
        bytes2 = []
        # str to int for common internal handling
        for i, byte in enumerate(bytes0):
            bytes2.append(ord(byte))
        sum_crc = checksum(bytes2[:-1])
        crc = sum_crc - bytes2[-1]
        if (sum_crc != bytes2[-1]):
            print ('CRC ERROR! calculated: {:02x} '.format(sum_crc) + ' - crc: {:02x} '.format(bytes2[-1]))
        if (bytes2[3] != 0):
            print ('DEVICE ERROR! '+'{:02x} '.format(bytes2[3]))
        #print (ord(bytes0[3]))
        # [0] == 0x0b, [1] == 0xff, [2] == length, [3] == error>0?
        print ('>: '+"".join('{:02x} '.format(x) for x in bytes2[4:-1]))
        return bytes0[4:-1]

ser = serial.Serial('/dev/tty.SLAB_USBtoUART', timeout=10)
print(ser.name)
#-----------------------------------------
# seen commands
# 20, 22, 25, 26, 40, 44, 60, 62, 65, 66, 68, 80, 82, 83, 85, 86, 87
print ("--?-- connect/disconnect?:")
send(ser, bytearray([0x20, 0x00]))
array_alpha = receive(ser)
print ("--.-- Version: major.minor")
send(ser, bytearray([0x22]), 0xfe)
array_alpha = receive(ser)
send(ser, bytearray([0x22]), 0xff)
array_alpha = receive(ser)
#for n in range(0x00, 0xff):
    #send(ser, bytearray([0x22]), n)
    #array_alpha = receive(ser)
print ("--.-- read dBm, continent (frequency) ")
# dBm: 0a-1e 10-30, continent: 00 china 920-925, 01 usa 902-928, 02 eu, 03 ? 868
send(ser, bytearray([0x26]))
array_alpha = receive(ser)
print ("--.-- write dBm, continent")
send(ser, bytearray([0x25, 0x0a, 0x02]))
array_alpha = receive(ser)
print ("--?-- read...")
send(ser, bytearray([0x44]))
array_alpha = receive(ser)
print ("--?-- ")
send(ser, bytearray([0x80, 0xff]))
array_alpha = receive(ser)
print ("--.-- identify EPC Gen2")
send(ser, bytearray([0x40, 0x07]))
array_alpha = receive(ser)
print ("--?-- read...")
send(ser, bytearray([0x44]))
array_alpha = receive(ser)
print ("--.-- read password, start, length double byte")
send(ser, bytearray([0x85, 0x00, 0x00, 0x08]))
array_alpha = receive(ser)
print ("--.-- read EPC")
send(ser, bytearray([0x85, 0x01, 0x00, 0x08]))
array_alpha = receive(ser)
print ("--.-- read TID")
send(ser, bytearray([0x85, 0x02, 0x00, 0x0c]))
array_alpha = receive(ser)
print ("--.-- read User")
send(ser, bytearray([0x85, 0x03, 0x00, 0x0d]))
array_alpha = receive(ser)
print ("--.-- read User")
send(ser, bytearray([0x85, 0x03, 0x10, 0x0d]))
array_alpha = receive(ser)
print ("--.-- write")
#                          area start #0   #1 .... 
#send(ser, bytearray([0x86, 0x01 0x02 0xe2 0x00]))
#array_alpha = receive(ser)
print ("--?-- read...")
send(ser, bytearray([0x44]))
array_alpha = receive(ser)
print ("--.-- ientify ISO18000-6B")
send(ser, bytearray([0x60]))
array_alpha = receive(ser)
print ("--?-- read...")
send(ser, bytearray([0x44]))
array_alpha = receive(ser)
print ("--?-- read ISO18000-6B adr 0 cnt 1")
send(ser, bytearray([0x68, 0x00]))
array_alpha = receive(ser)
print ("--.-- write ISO18000-6B adr 0 0x00")
#send(ser, bytearray([0x62, 0x00, 0x00]))
#array_alpha = receive(ser)
print ("--.-- write ISO18000-6B adr 1 0x00")
#send(ser, bytearray([0x62, 0x01, 0x00]))
#array_alpha = receive(ser)
print ("--.-- lock ISO18000-6B")
#send(ser, bytearray([0x65, 0x00]))
#array_alpha = receive(ser)
print ("--.-- query ISO18000-6B")
send(ser, bytearray([0x66, 0x00]))
array_alpha = receive(ser)
print ("--.-- fast write")
#send(ser, bytearray([0x87, 0x01, 0x00, 0x01, 0xe7, 0xe6]))
#array_alpha = receive(ser)
print ("--.-- lock")
#send(ser, bytearray([0x82, 0x01, 0x00]))
#array_alpha = receive(ser)
print ("--.-- kill")
#send(ser, bytearray([0x83, 0x00, 0x00, 0x01, 0x23]))
#array_alpha = receive(ser)

#for x in array_alpha:
    #print ('{:02x}'.format(ord(x)))
#-----------------------------------------
