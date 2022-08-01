from threading import Thread
import time
from random import randint
from numpy import array
from threading import Lock
import sqlite3

p = 13

conSQ = sqlite3.connect('TestDatenbank')
curSQ = conSQ.cursor()
curSQ.execute('''CREATE TABLE IF NOT EXISTS tshirts (productnumber text, name text, size text, price real)''')
curSQ.execute('''INSERT INTO tshirts VALUES('1234','black','M','p')''')
conSQ.commit()
for row in curSQ.execute('''SELECT * FROM tshirts'''):
    row

lock = Lock()

class DevicesTCP(Thread):
    def __init__(self,name,IPadr,port):
        super().__init__()
        self.name   = name
        self.IPadr  = IPadr
        self.port   = port

class WRpv(DevicesTCP):
    def __init__(self,name,IPadr,port):
        super().__init__(name, IPadr,port)

    def get_P(self):
        return randint(0,10)

    def run(self):
        for a in range(3):
            lock.acquire()
            print(self.name,'-> P =',self.get_P(),'kW')
            lock.release()
            time.sleep(2)

class WRbat(DevicesTCP):
    def __init__(self,name,IPadr,port):
        super().__init__(name,IPadr,port)

    def get_SoC(self):
        return randint(0,100)

    def run(self):
        for b in range(3):
            lock.acquire()
            print(self.name,'-> SoC =',self.get_SoC(),'%')
            lock.release()
            time.sleep(2)

class Load(Thread):
    def __init__(self,name,IPadr,port):
        super().__init__()
        self.name   = name
        self.IPadr  = IPadr
        self.port   = port

    def get_L(self):
        return randint(0,10)

    def run(self):
        for a in range(3):
            lock.acquire()
            print(self.name,'-> Last =',self.get_L(),'kW')
            lock.release()
            time.sleep(2)

device1 = WRpv('PV-Wechselrichter','134.169.132.230','502')
device2 = WRbat('Bat-Wechselrichter','134.169.132.4','502')
device3 = Load('Haushaltslast','123.345.668.123','502')



devices = [device1,device2,device3]
for dev in devices:
    dev.start()


#device1.start()
#device2.start()

