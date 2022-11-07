import time
import datetime
import sqlite3
from threading import Thread
import csv


class PVprofil(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_pv
        csv_file = open('Sunny_12bis18Uhr_2021Jun17.csv',newline='')
        pv_profile = csv.DictReader(csv_file,delimiter=';')
        for row in pv_profile:
            if row['P_TOTAL'] == '':
                time.sleep(0.99)
            else:
                P_pv = float(row['P_TOTAL'])
                print(round(P_pv))
            time.sleep(0.99)

class Database(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(0,86400):
            time.sleep(1)
            global P_pv
            path = 'CSV-Reinigung.db'
            timestamp = datetime.datetime.now()
            Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))


            conSQ = sqlite3.connect(path)
            curSQ = conSQ.cursor()
            curSQ.execute("CREATE TABLE IF NOT EXISTS T1 (Timestamp text, P_PV real)")
            curSQ.execute("INSERT INTO T1 (Timestamp, P_PV) VALUES (?,?)",(Timestamp, P_pv))
            conSQ.commit()

            for row in curSQ.execute("SELECT * FROM T1"):
                row

csv_pv = PVprofil()
data = Database()

concurrentthreads = [csv_pv,data]
for threads in concurrentthreads:
    threads.start()





