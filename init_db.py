#!flask/bin/python
from app import  db, models
import datetime, time, random#, smbus

temp = models.Tempdata(data1=20,data2=23,timestamp=datetime.datetime.utcnow())
db.session.add(temp)
conf = models.Conf(tresh1=20,tresh2=21,updateinsec=10,relstate=0)
db.session.add(conf)
db.session.comit()

