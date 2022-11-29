import sqlite3
import time
from threading import Thread

def Energieberechnung():
    E_bat = 0
    for Durchlauf in range (0,3600):
        P = 1000 # W
        E_bat = (E_bat + (P * 1/3600))
        print('E_bat =',round(E_bat),'Wh -> Durchlauf - ', Durchlauf)
        #time.sleep(1)
#Energieberechnung()

class Database(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global market_WE1
        while True:
            conn = sqlite3.connect('marketDB_sim.db')
            cc = conn.cursor()

            cc.execute('SELECT * FROM MarktTabelle')
            value = cc.fetchall()

            market_WE1 = value[1][1]
            market_WE2 = value[2][1]
            market_WE3 = value[3][1]
            market_WE4 = value[4][1]

            #print(market_WE3)

            time.sleep(1)

class BSS_virtuell(Thread):
    def __init__(self,marketvalue,P_pv_v):
        super().__init__()
        self.marketvalue = marketvalue
        self.P_pv_v = P_pv_v

    def run(self):
        while True:
            try:
                #self.marketvalue = 'Normal'
                print('Objekteinstellung -> ', WE1.marketvalue)


            except NameError as err:
                print('NameError ->',str(err))
                pass
            time.sleep(1)



market_WE = 'Normal'
WE1 = BSS_virtuell(market_WE,5)
data = Database()

concurrentthreads = [data,WE1]
for threads in concurrentthreads:
    threads.start()



