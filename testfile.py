# Energiekonto für jeden Haushalt
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
                time.sleep(1)
            else:
                P_tot = float(row['P_TOTAL'])
                P_pv = round((2/7) * P_tot) # W
                #print(P_pv)
            time.sleep(1)

class Lastprofil(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_Last
        csv_file = open('LP17_2010-06-23_12.00.00_to_2010-06-23_18.00.00_Mi.csv',newline='')
        load_profile = csv.DictReader(csv_file,delimiter=',')
        for row in load_profile:
            P1 = float(row['P1'])
            P2 = float(row['P2'])
            P3 = float(row['P3'])
            P_Last = P1+P2+P3
            #print(row['Timestamp'],'--->',P_soll,'W')
            time.sleep(1)

class Energiekonto(Thread):
    def __init__(self,Wohneinheit,P_bat_v,E_bat,betrag,P_load,load_offset,P_Netz_v):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.P_bat_v = P_bat_v
        self.E_bat = E_bat
        self.betrag = betrag
        self.P_load = P_load
        self.load_offset = load_offset
        self.P_Netz_v = P_Netz_v

    def buchen(self):
        global P_Last
        global P_pv
        global P_batWE

        self.P_load = P_Last*self.load_offset
        dE_bat = (-self.P_load * (1/3600)) + (P_pv * (1/3600))
        self.betrag = dE_bat

        if self.E_bat + self.betrag <= 0:
            print('Energiekonto von',self.Wohneinheit,'leer, setze Entladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load - P_pv - self.P_bat_v


        elif self.E_bat + self.betrag >= 3167:
            print('Energiekonto von',self.Wohneinheit, 'ist voll, setze Ladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load - P_pv - self.P_bat_v

        else:
            self.E_bat = self.E_bat + self.betrag
            self.P_bat_v = self.P_load - P_pv       # bei PV-Überschuss negativer Wert -> Speicher laden!
            self.P_Netz_v = self.P_load - P_pv - self.P_bat_v

    def anzeigen(self):
        Energiekonto = round(self.E_bat,2)
        WE = self.Wohneinheit
        vSoC = round((self.E_bat/3167)*100,2)
        return WE,Energiekonto,vSoC # - , Wh, %

    def write_Database(self):
        global P_pv
        global P_bat_real
        path = 'MomentanwertDB_test1.db'
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        E_bat_sum = round(WE1.E_bat + WE2.E_bat + WE3.E_bat + WE4.E_bat + WE5.E_bat,1)
        SoC_sum = round((E_bat_sum/(3167*5))*100,1)
        P_load_sum = round(WE1.P_load + WE2.P_load + WE3.P_load + WE4.P_load + WE5.P_load,1)
        P_Netz_sum = round(WE1.P_Netz_v + WE2.P_Netz_v + WE3.P_Netz_v + WE4.P_Netz_v + WE5.P_Netz_v,1)
        value_list = [
                    (Timestamp,'Gerätewerte',E_bat_sum,SoC_sum,P_bat_real,P_load_sum,P_pv*5, P_Netz_sum),
                    (Timestamp,WE1.Wohneinheit, round(WE1.E_bat,1), round((WE1.E_bat / 3167) * 100, 1),WE1.P_bat_v, WE1.P_load, P_pv, WE1.P_Netz_v),
                    (Timestamp,WE2.Wohneinheit, round(WE2.E_bat,1), round((WE2.E_bat / 3167) * 100, 1),WE2.P_bat_v, WE2.P_load, P_pv, WE2.P_Netz_v),
                    (Timestamp,WE3.Wohneinheit, round(WE3.E_bat,1), round((WE3.E_bat / 3167) * 100, 1),WE3.P_bat_v, WE3.P_load, P_pv, WE3.P_Netz_v),
                    (Timestamp,WE4.Wohneinheit, round(WE4.E_bat,1), round((WE4.E_bat / 3167) * 100, 1),WE4.P_bat_v, WE4.P_load, P_pv, WE4.P_Netz_v),
                    (Timestamp,WE5.Wohneinheit, round(WE5.E_bat,1), round((WE5.E_bat / 3167) * 100, 1),WE5.P_bat_v, WE5.P_load, P_pv, WE5.P_Netz_v)
                      ]
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute("CREATE TABLE IF NOT EXISTS aTest2 "
                      "(Timestamp text, x text PRIMARY KEY,E_bat real, SoC real,P_BSS real, P_Last real,P_PV real, P_Netz real)")
        curSQ.executemany("INSERT OR REPLACE INTO aTest2 "
                          "(Timestamp, x, E_bat, SoC,P_BSS, P_Last,P_PV, P_Netz) VALUES (?,?,?,?,?,?,?,?)",(value_list))
        conSQ.commit()
        for row in curSQ.execute("SELECT * FROM aTest2"):
            row

    def run(self):
        global P_pv
        global P_bat_real
        while True:
            try:
                #print(WE1.anzeigen(),'W .. P_Last1 =',WE1.P_load, '|',WE2.anzeigen(),'W .. P_Last2 =',WE2.P_load,'---> Zur Prüfung WE2_betrag =',WE2.betrag,'--->--->---> P_pv_WE =',round(P_pv))
                WE1.buchen()
                WE2.buchen()
                WE3.buchen()
                WE4.buchen()
                WE5.buchen()

                P_bat_real = round(WE1.P_bat_v + WE2.P_bat_v + WE3.P_bat_v + WE4.P_bat_v + WE5.P_bat_v,1)
                print('Summierte Werte -> P_bat_real =',P_bat_real,'W , P_pv =',P_pv*5,'W')

                self.write_Database()


            except NameError as err:
                #print('NameError -->',str(err))
                pass
            time.sleep(1)

PVabfrage = PVprofil()
Lastabfrage = Lastprofil() #Lastprofil 17 -> Verbrauch 6000 kWh im Jahr
WE1 = Energiekonto('WE1',0,2220,0,0,0.6,0)  #WE,P_bat_r, Energiekonto, betrag,P_load, load_offset
WE2 = Energiekonto('WE2',0,2800,0,0,0.75,0) #Angabe in Wh
WE3 = Energiekonto('WE3',0,3150,0,0,0.7,0)
WE4 = Energiekonto('WE4',0,1900,0,0,1.3,0)
WE5 = Energiekonto('WE5',0,2100,0,0,1.0,0)

concurrentthreads = [Lastabfrage,PVabfrage,WE1]
for threads in concurrentthreads:
    threads.start()



# Möglichkeiten für regelmäßige Synchronisation/Kalibrierung ???
#       - Ungenauigkeit durch Verluste
#       - Ungenauigkeit durch sekündliche Energieflussberechnung
#   LÖSUNG: Summierte Werte und Geräte-Auslesewerte regelmäßig gegenüberstellen und Differenz gleichmäßig auf alle WE aufteilen
