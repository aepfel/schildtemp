# -*- coding: utf-8 -*-
import smbus
import time
bus = smbus.SMBus(1)
address = 0x77


def signed(value):
        if value > 32767:
                value -= 65536
        return value


def read_temp():
    #start messurement
    register = 0xF4
    value = 0x2E
    bus.write_byte_data(address, register, value)
    time.sleep(0.005)
    #uncompressed temperature
    UT = (bus.read_byte_data(address, 0xF6) << 8) +  bus.read_byte_data(address, 0xF7)
    #UT = 27898 #testdata
    #calculate
    X1 = ((UT - AC6) * AC5) >> 15
    X2 = (MC << 11) / (X1 + MD)
    global B5 
    B5 = X1 + X2
    T = ((B5 + 8) >> 4)/10.0
    return(T)

def read_pressure():
    #start messurement
    register = 0xF4
    value = 0x34 + (Oss<<6)
    bus.write_byte_data(address, register, value)
    time.sleep(0.005)
    #uncompressed pressure
    UP_MSB = bus.read_byte_data(address, 0xF6)
    UP_LSB = bus.read_byte_data(address, 0xF7)
    UP_XLSB = bus.read_byte_data(address, 0xF8)
    UP = ((UP_MSB<<16) + (UP_LSB<<8) + UP_XLSB) >> (8-Oss)
    #UP = 23843 #testdata
    #calculate
    B6 = B5 - 4000
    X1 = (B2*((B6*B6 >> 12))) >> 11
    X2 = (AC2*B6) >> 11
    X3 = X1 + X2
    B3 = (((AC1*4+X3)<<Oss)+2)/4
    X1 = (AC3*B6) >> 13
    X2 = (B1*((B6*B6)>>12))>>16
    X3 = ((X1+X2)+2) >> 2
    B4 = (AC4*(X3+32768)) >> 15
    B7 = (UP-B3)*(50000>>Oss)
    p = (B7/B4)*2
    if (B7 < 0x80000000): 
	p = (B7*2)/B4
    X1 = (p>>8)*(p>>8)
    X1 = (X1*3038)>>16
    X2 = (-7357*p)>>16
    P = p + (X1+X2+3791)/2**4
    return(P/100)

#testdata from bosch-duko
def test():
    global AC1, AC2, AC3, AC4,AC5,AC6,B1,B2,MB,MC,MD,Oss
    AC1 = 408
    AC2 = -72
    AC3 = -14383
    AC4 = 32741
    AC5 = 32757
    AC6 = 23153
    B1 = 6190
    B2 = 4
    MB = -32768
    MC = -8711
    MD = 2868
    Oss = 0

#print init-register-data    
def print_reg():
    print(AC1)
    print(AC2)
    print(AC3)
    print(AC4)
    print(AC5)
    print(AC6)
    print(B1)
    print(B2)
    print(MB)
    print(MC)
    print(MD)

    

AC1 = signed((bus.read_byte_data(address, 0xAA) << 8) + bus.read_byte_data(address, 0XAB))
AC2 = signed((bus.read_byte_data(address, 0xAC) << 8) + bus.read_byte_data(address, 0XAD))
AC3 = signed((bus.read_byte_data(address, 0xAE) << 8) + bus.read_byte_data(address, 0XAF))
AC4 = (bus.read_byte_data(address, 0xB0) << 8) + bus.read_byte_data(address, 0XB1)
AC5 = (bus.read_byte_data(address, 0xB2) << 8) + bus.read_byte_data(address, 0XB3)
AC6 = (bus.read_byte_data(address, 0xB4) << 8) + bus.read_byte_data(address, 0XB5)
B1 = signed((bus.read_byte_data(address, 0xB6) << 8) + bus.read_byte_data(address, 0XB7))
B2 = signed((bus.read_byte_data(address, 0xB8) << 8) + bus.read_byte_data(address, 0XB9))
MB = signed((bus.read_byte_data(address, 0xBA) << 8) + bus.read_byte_data(address, 0XBB))
MC = signed((bus.read_byte_data(address, 0xBC) << 8) + bus.read_byte_data(address, 0XBD))
MD = signed((bus.read_byte_data(address, 0xBE) << 8) + bus.read_byte_data(address, 0XBF))
Oss = bus.read_byte_data(address,0XF4) & 0xC0
Sco = bus.read_byte_data(address,0XF4) & 0x20


while True:
    #test()
    print("Temperatur:" + str(read_temp()) + "°C")
    print("Luftdruck:" + str(read_pressure()) + "hPa")
    time.sleep(10)

