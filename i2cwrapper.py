# -*- coding: utf-8 -*-
import smbus
import os

#wrapper für i2c-busabfragen
#soll synchrones belegen des busses verhindern
#benoetigt zur initalisierung die adresse des busses(2)
class Wrapper(object):
    locked = False
    fehler=[0,0]

    def __init__(self, y=2):
	self.bus = smbus.SMBus(y)
        self.w_queue = []
        self.r_queue = []
        self.locked = False

    def write(self, caddress, raddress, value):
        self.w_queue.append([caddress, raddress, value])
        return self.set_d()

    def read(self, caddress, raddress):
        self.r_queue.append([caddress, raddress])
        return self.get_d()

    def set_d(self):
        global fehler
        self.fehler[0] += 1
        while not ('d' in locals()):
            if not self.locked:
                d = self.w_queue.pop(0)
                self.locked = True
                try:
                    self.bus.write_byte_data(d[0],d[1],d[2])
                    self.locked = False
                except Exception as e:
                    self.fehler[1]+=1
                    print("Schreibfehler:{0}\nPID:{1} Fehler:{2},{2}".format(e,os.getpid(),self.fehler[0],self.fehler[1]))                    
                self.locked = False
        return d

    def get_d(self):
        d = self.r_queue.pop(0)
        while not ('v' in locals()):
            if not self.locked:
                self.locked = True
                try:
                    v = self.bus.read_byte_data(d[0],d[1])
                except Exception as e:
                    print("Schreibfehler:{0}".format(e))
                self.locked = False
        return v

