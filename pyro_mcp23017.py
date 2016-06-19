# ~~ coding: utf-8 ~~
import time
import i2cwrapper
import Pyro4

class mcp23017(object):

  def __init__(self, y = 1):
    self.y = y
    self.bus = i2cwrapper.Wrapper(y) # Rev 2 Pi uses 1
    bus = self.bus
    self.DEVICE = 0x20 # Device address (A0-A2)
    self.IODIRA = 0x00 # Pin direction register
    self.IODIRB = 0x01 # Pin direction register
    self.OLATA  = 0x14 # Register for outputs
    self.GPIOA  = 0x12 # Register for inputs
    self.OLATB  = 0x15 # Register for outputs
    self.GPIOB  = 0x13 # Register for inputs
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
    bus.write(self.DEVICE,self.IODIRA,0x00)
    bus.write(self.DEVICE,self.IODIRB,0x00)
# Set output all 7 output bits to 0
    bus.write(self.DEVICE,self.OLATA,0x00)
    bus.write(self.DEVICE,self.OLATB,0x00)

#for MyData in range(1,8):
  #Count from 1 to 8 which in binary will count
  #from 001 to 111
  #bus.write_byte_data(DEVICE,OLATA,MyData)
  #print MyData
  #time.sleep(1)

# Set all bits to zero
  def all_off(self):
      self.bus.write(self.DEVICE,self.OLATA,0xff) #benutzt für relaise mit negativer logik
      self.bus.write(self.DEVICE,self.OLATA,0xff)

  def set_a(self, val = 0xFF):
      self.bus.write(self.DEVICE,self.OLATA,val)
	
  def set_b(self, val = 0xFF):
      self.bus.write(self.DEVICE,self.OLATB,val)


## -- pyrocode starts here -- ##
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(mcp23017)
ns.register("terrarium.relais",uri)

print("Bereit.")
daemon.requestLoop()

