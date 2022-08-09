#import sqlite3
#path = 'database/data2.db'
#conn = sqlite3.connect(path)
#conn.close()
#curSQ = conSQ.cursor()

import devices.PVinverter.PVinverter as PV
import devices.BATinverter.BATinverter as BAT
import database.database as DB

PVinverter  = PV.WRpv('PV-Inverter','134.169.132.235','502')
BATinverter = BAT.WRbat('BAT-Inverter','134.169.132.234','502')
database = DB.Database('Actual Value database')

concurrentthreads = [PVinverter,BATinverter,database]
for threads in concurrentthreads:
    threads.start()