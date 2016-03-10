#!flask/bin/python
from app import  db, models
import datetime, time, random#, smbus
from schalten import schalten
#bus=smbus.SMBus(2)
#address=0x20
#bus.write_byte_data(address,0x0c,0xff) #pullup aktivieren
#bus.write_byte_data(address,0x0d,0xff) #pullup aktivieren


# todo:
# smbus import 
# tempsensor und relaise lesen/schrien


# relaise schalten mit mask: 0=nix,1=erstes,2=zweites,3=erstes und zweites,4=drittes, usw.
#def schalten(mask = 0):
 #   print(mask)
    #bus.write_byte_data(address,1,mask)
  #  return()

# temperatur von sensor holen
def sensor():
    # dummys fuer noch nicht fuhelbare sensordaten
    s1 = random.randint(10,500)
    s2 = random.randint(10,500)
    return(s1,s2)


while True:
    conf = models.Conf.query.get(1)
    t1 = conf.tresh1
    t2 = conf.tresh2
    warten = conf.updateinsec
    s1, s2 = sensor()
    temphist = models.Tempdata(data1=s1,data2=s2,timestamp=datetime.datetime.utcnow())
    db.session.add(temphist)
    if (s1<t1):
        schalten(170)
        conf.relstate = 170
    else:
        schalten(0)
        conf.relstate = 0
    db.session.commit()
    time.sleep(warten)


