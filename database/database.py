import sqlite3
from threading import Thread
import datetime
import devices.PVinverter.PVinverter as PV
import devices.BATinverter.BATinverter as BAT
import time


class Database(Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def WRpv_write_Database(self):
        path = 'database/DATENBANK.db'
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        Devicename = 'PV-WR'
        P = PV.WRpv.get_P(self)
        Anmerkung = 'Werte schreiben'
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute('''CREATE TABLE IF NOT EXISTS WRpv (Timestamp text, Devicename text, P real, Anmerkung text)''')
        curSQ.execute('''INSERT INTO WRpv (Timestamp, Devicename, P, Anmerkung) VALUES (?,?,?,?) ''',(Timestamp, Devicename, P, Anmerkung))
        conSQ.commit()
        for row in curSQ.execute('''SELECT * FROM WRpv'''):
            row

    def WRbat_write_Database(self):
        path = 'database/DATENBANK.db'
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        Devicename = 'BAT-WR'
        SoC = BAT.WRbat.get_SoC(self)
        Temp = BAT.WRbat.get_Temp(self)
        Anmerkung = 'Batteriewerte'
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute('''CREATE TABLE IF NOT EXISTS WRbat (Timestamp text, Devicename text, SoC real, Temp real, Anmerkung text)''')
        curSQ.execute('''INSERT INTO WRbat (Timestamp, Devicename, SoC, Temp, Anmerkung) VALUES (?,?,?,?,?) ''',(Timestamp, Devicename, SoC, Temp, Anmerkung))
        conSQ.commit()
        for row in curSQ.execute('''SELECT * FROM WRbat'''):
            row

    def run(self):
        for i in range(0,5):
            time.sleep(2)
            self.WRpv_write_Database()
            self.WRbat_write_Database()