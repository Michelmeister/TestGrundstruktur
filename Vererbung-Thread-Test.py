from threading import Thread
import time
import datetime
from random import randint
from numpy import array
from threading import Lock
import sqlite3


#lock = Lock()

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
        self.name
        self.get_P()
        time.sleep(0.2)
        #for a in range(1):
            #lock.acquire()
            #print(self.name,'-> P =',self.get_P(),'kW')
            #lock.release()
        #while True:
            #self.write_Database()
            #if WRbat.get_SoC(self) < 50:
                #print('Test funktioniert und SoC beträgt :' ,WRbat.get_SoC(self))
            #time.sleep(1)
class WRbat(DevicesTCP):
    def __init__(self,name,IPadr,port):
        super().__init__(name,IPadr,port)

    def get_SoC(self):
        return 47

    def get_Temp(self):
        return randint(20,27)

    def run(self):
            while True:
                self.get_SoC()
                self.get_Temp()
                time.sleep(0.2)
class Load(Thread):
    def __init__(self,name,IPadr,port):
        super().__init__()
        self.name   = name
        self.IPadr  = IPadr
        self.port   = port

    def get_L(self):
        return randint(0,5)

    def run(self):
        self.get_L()
        time.sleep(0.2)
        #for a in range(1):
         #   lock.acquire()
          #  print(self.name,'-> Last =',self.get_L(),'kW')
           # lock.release()
            #time.sleep(0.2)
class Database(Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def WRpv_write_Database(self):
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        Devicename = 'PV-WR'
        P = WRpv.get_P(self)
        Anmerkung = 'Databaseclass write'
        conSQ = sqlite3.connect('DBinMethode.db')
        curSQ = conSQ.cursor()
        curSQ.execute('''CREATE TABLE IF NOT EXISTS WRpv (Timestamp text, Devicename text, P real, Anmerkung text)''')
        curSQ.execute('''INSERT INTO WRpv (Timestamp, Devicename, P, Anmerkung) VALUES (?,?,?,?) ''',(Timestamp, Devicename, P, Anmerkung))
        conSQ.commit()
        for row in curSQ.execute('''SELECT * FROM WRpv'''):
            row

    def WRbat_write_Database(self):
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        Devicename = 'BAT-WR'
        SoC = WRbat.get_SoC(self)
        Temp = WRbat.get_Temp(self)
        Anmerkung = 'Databaseclass write'
        conSQ = sqlite3.connect('DBinMethode.db')
        curSQ = conSQ.cursor()
        curSQ.execute('''CREATE TABLE IF NOT EXISTS WRbat (Timestamp text, Devicename text, SoC real, Temp real, Anmerkung text)''')
        curSQ.execute('''INSERT INTO WRbat (Timestamp, Devicename, SoC, Temp, Anmerkung) VALUES (?,?,?,?,?) ''',(Timestamp, Devicename, SoC, Temp, Anmerkung))
        conSQ.commit()
        for row in curSQ.execute('''SELECT * FROM WRbat'''):
            row

    def Load_write_Database(self):
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        Devicename = 'Momentanlast'
        L = Load.get_L(self)
        Anmerkung = 'Databaseclass write Load'
        conSQ = sqlite3.connect('DBinMethode.db')
        curSQ = conSQ.cursor()
        curSQ.execute('''CREATE TABLE IF NOT EXISTS Load (Timestamp text, Devicename text, L real, Anmerkung text)''')
        curSQ.execute('''INSERT INTO Load (Timestamp, Devicename, L, Anmerkung) VALUES (?,?,?,?) ''',(Timestamp, Devicename, L, Anmerkung))
        conSQ.commit()
        for row in curSQ.execute('''SELECT * FROM Load'''):
            row

    def run(self):
        while True:
            time.sleep(3)
            self.WRpv_write_Database()
            self.WRbat_write_Database()
            self.Load_write_Database()

database1 = Database('WRpvDatenbank')
device1 = WRpv('PV-Wechselrichter','134.169.132.230','502')
device2 = WRbat('Bat-Wechselrichter','134.169.132.4','502')
device3 = Load('Haushaltslast','123.345.668.123','502')

concurrentthreads = [device1,device2,device3,database1]
for threads in concurrentthreads:
    threads.start()
print('While-loop running')

#addition(1,2,3,4)
#device1.start()
#device2.start()













