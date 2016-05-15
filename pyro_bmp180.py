# -*- coding: utf-8 -*-
import smbus
import time
import Pyro4

class bmp180(object):

  def signed(self, value):
        if value > 32767:
                value -= 65536
        return value


  def __init__(self, y=1):
        self.y = y
        bus = smbus.SMBus(y)
        self.bus = bus
        self.address = 0x77
        address = self.address
        self.AC1 = self.signed((bus.read_byte_data(address, 0xAA) << 8) + bus.read_byte_data(address, 0XAB))
        self.AC2 = self.signed((bus.read_byte_data(address, 0xAC) << 8) + bus.read_byte_data(address, 0XAD))
        self.AC3 = self.signed((bus.read_byte_data(address, 0xAE) << 8) + bus.read_byte_data(address, 0XAF))
        self.AC4 = (bus.read_byte_data(address, 0xB0) << 8) + bus.read_byte_data(address, 0XB1)
        self.AC5 = (bus.read_byte_data(address, 0xB2) << 8) + bus.read_byte_data(address, 0XB3)
        self.AC6 = (bus.read_byte_data(address, 0xB4) << 8) + bus.read_byte_data(address, 0XB5)
        self.B1 = self.signed((bus.read_byte_data(address, 0xB6) << 8) + bus.read_byte_data(address, 0XB7))
        self.B2 = self.signed((bus.read_byte_data(address, 0xB8) << 8) + bus.read_byte_data(address, 0XB9))
        self.MB = self.signed((bus.read_byte_data(address, 0xBA) << 8) + bus.read_byte_data(address, 0XBB))
        self.MC = self.signed((bus.read_byte_data(address, 0xBC) << 8) + bus.read_byte_data(address, 0XBD))
        self.MD = self.signed((bus.read_byte_data(address, 0xBE) << 8) + bus.read_byte_data(address, 0XBF))
        self.Oss = bus.read_byte_data(address,0XF4) & 0xC0
        self.Sco = bus.read_byte_data(address,0XF4) & 0x20
        self.B5 = 0

        

  def read_temp(self):
    #start messurement
    address = self.address
    register = 0xF4
    value = 0x2E
    bus = self.bus
    bus.write_byte_data(address, register, value)
    time.sleep(0.005)
    #uncompressed temperature
    UT = (bus.read_byte_data(address, 0xF6) << 8) +  bus.read_byte_data(address, 0xF7)
    #UT = 27898 #testdata
    #calculate
    X1 = ((UT - self.AC6) * self.AC5) >> 15
    X2 = (self.MC << 11) / (X1 + self.MD)
    self.B5 = X1 + X2
    T = ((self.B5 + 8) >> 4)/10.0
    return(T)

  def read_pressure(self):
    #start messurement
    address = self.address
    register = 0xF4
    value = 0x34 + (self.Oss<<6)
    bus = self.bus
    bus.write_byte_data(address, register, value)
    time.sleep(0.005)
    #uncompressed pressure
    UP_MSB = bus.read_byte_data(address, 0xF6)
    UP_LSB = bus.read_byte_data(address, 0xF7)
    UP_XLSB = bus.read_byte_data(address, 0xF8)
    UP = ((UP_MSB<<16) + (UP_LSB<<8) + UP_XLSB) >> (8 - self.Oss)
    #UP = 23843 #testdata
    #calculate
    B6 = self.B5 - 4000
    X1 = (self.B2*((B6*B6 >> 12))) >> 11
    X2 = (self.AC2*B6) >> 11
    X3 = X1 + X2
    B3 = (((self.AC1*4+X3) << self.Oss)+2)/4
    X1 = (self.AC3*B6) >> 13
    X2 = (self.B1*((B6*B6)>>12))>>16
    X3 = ((X1+X2)+2) >> 2
    B4 = (self.AC4*(X3+32768)) >> 15
    B7 = (UP-B3)*(50000 >> self.Oss)
    p = (B7/B4)*2
    if (B7 < 0x80000000): 
	p = (B7*2)/B4
    X1 = (p>>8)*(p>>8)
    X1 = (X1*3038)>>16
    X2 = (-7357*p)>>16
    P = p + (X1+X2+3791)/2**4
    return(P/100)

#testdata from bosch-duko
  def test(self):
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
  def print_reg(self):
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

    

  def permaprint(self, t=1):
    while True:
      #test()
      print("Temperatur:" + str(self.read_temp()) + "°C")
      print("Luftdruck:" + str(self.read_pressure()) + "hPa")
      time.sleep(t)

#sensor = bmp180(1)
#sensor.permaprint()
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(bmp180)
ns.register("terrarium.sensor",uri)

print("Bereit.")
daemon.requestLoop()
