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
        global Timestamp_sim

        csv_file = open('PV_2021-03-23_18.00.00_to_23.59.59_cloudy.csv',newline='')
        pv_profile = csv.DictReader(csv_file,delimiter=',')
        for row in pv_profile:
            if row['P_TOTAL'] == '':
                #time.sleep(1)
                pass
            else:
                P_tot = float(row['P_TOTAL'])
                P_pv = round((2/7) * P_tot) # W
                #print(P_pv)
            Timestamp_sim = (row['Timestamp'])
            time.sleep(1)

class Lastprofil(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_Last
        csv_file = open('LP17_2010-06-23_18.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
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
            #print('Energiekonto von',self.Wohneinheit,'leer, setze Entladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load - P_pv - self.P_bat_v


        elif self.E_bat + self.betrag >= 3167:
            #print('Energiekonto von',self.Wohneinheit, 'ist voll, setze Ladeleistung P_bat = 0')
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
        E_bat_sum = round(WE1.E_bat + WE2.E_bat + WE3.E_bat + WE4.E_bat + WE5.E_bat + WE6.E_bat + WE7.E_bat + WE8.E_bat + WE9.E_bat + WE10.E_bat
                          + WE11.E_bat + WE12.E_bat + WE13.E_bat + WE14.E_bat + WE15.E_bat + WE16.E_bat + WE17.E_bat + WE18.E_bat + WE19.E_bat + WE20.E_bat
                          + WE21.E_bat + WE22.E_bat + WE23.E_bat + WE24.E_bat + WE5.E_bat,1)
        SoC_sum = round((E_bat_sum/(76008))*100,1)
        P_load_sum = round(WE1.P_load + WE2.P_load + WE3.P_load + WE4.P_load + WE5.P_load + WE6.P_load + WE7.P_load + WE8.P_load + WE9.P_load + WE10.P_load
                           + WE11.P_load + WE12.P_load + WE13.P_load + WE14.P_load + WE15.P_load + WE16.P_load + WE17.P_load + WE18.P_load + WE19.P_load + WE20.P_load
                           + WE21.P_load + WE22.P_load + WE23.P_load + WE24.P_load,1)
        P_Netz_sum = round(WE1.P_Netz_v + WE2.P_Netz_v + WE3.P_Netz_v + WE4.P_Netz_v + WE5.P_Netz_v + WE6.P_Netz_v + WE7.P_Netz_v + WE8.P_Netz_v + WE9.P_Netz_v + WE10.P_Netz_v
                           + WE11.P_Netz_v + WE12.P_Netz_v + WE13.P_Netz_v + WE14.P_Netz_v + WE15.P_Netz_v + WE16.P_Netz_v + WE17.P_Netz_v + WE18.P_Netz_v + WE19.P_Netz_v + WE20.P_Netz_v
                           + WE21.P_Netz_v + WE22.P_Netz_v + WE23.P_Netz_v + WE24.P_Netz_v,1)

        value_list = [
                    (Timestamp,'SummenWerte',E_bat_sum,SoC_sum,P_bat_real,P_load_sum,P_pv*24, P_Netz_sum),
                    (Timestamp,WE1.Wohneinheit, round(WE1.E_bat,1), round((WE1.E_bat / 3167) * 100, 1),WE1.P_bat_v, WE1.P_load, P_pv, WE1.P_Netz_v),
                    (Timestamp,WE2.Wohneinheit, round(WE2.E_bat,1), round((WE2.E_bat / 3167) * 100, 1),WE2.P_bat_v, WE2.P_load, P_pv, WE2.P_Netz_v),
                    (Timestamp,WE3.Wohneinheit, round(WE3.E_bat,1), round((WE3.E_bat / 3167) * 100, 1),WE3.P_bat_v, WE3.P_load, P_pv, WE3.P_Netz_v),
                    (Timestamp,WE4.Wohneinheit, round(WE4.E_bat,1), round((WE4.E_bat / 3167) * 100, 1),WE4.P_bat_v, WE4.P_load, P_pv, WE4.P_Netz_v),
                    (Timestamp,WE5.Wohneinheit, round(WE5.E_bat,1), round((WE5.E_bat / 3167) * 100, 1),WE5.P_bat_v, WE5.P_load, P_pv, WE5.P_Netz_v),
                    (Timestamp,WE6.Wohneinheit, round(WE6.E_bat,1),round((WE6.E_bat / 3167) * 100, 1),WE6.P_bat_v,WE6.P_load, P_pv, WE6.P_Netz_v),
                    (Timestamp,WE7.Wohneinheit, round(WE7.E_bat, 1), round((WE7.E_bat / 3167) * 100, 1), WE7.P_bat_v,WE7.P_load, P_pv, WE7.P_Netz_v),
                    (Timestamp, WE8.Wohneinheit, round(WE8.E_bat, 1), round((WE8.E_bat / 3167) * 100, 1), WE8.P_bat_v,WE8.P_load, P_pv, WE8.P_Netz_v),
                    (Timestamp, WE9.Wohneinheit, round(WE9.E_bat, 1), round((WE9.E_bat / 3167) * 100, 1), WE9.P_bat_v,WE9.P_load, P_pv, WE9.P_Netz_v),
                    (Timestamp, WE10.Wohneinheit, round(WE10.E_bat, 1), round((WE10.E_bat / 3167) * 100, 1), WE10.P_bat_v,WE10.P_load, P_pv, WE10.P_Netz_v),
                    (Timestamp, WE11.Wohneinheit, round(WE11.E_bat, 1), round((WE11.E_bat / 3167) * 100, 1), WE11.P_bat_v,WE11.P_load, P_pv, WE11.P_Netz_v),
                    (Timestamp, WE12.Wohneinheit, round(WE12.E_bat, 1), round((WE12.E_bat / 3167) * 100, 1), WE12.P_bat_v,WE12.P_load, P_pv, WE12.P_Netz_v),
                    (Timestamp, WE13.Wohneinheit, round(WE13.E_bat, 1), round((WE13.E_bat / 3167) * 100, 1), WE13.P_bat_v,WE13.P_load, P_pv, WE13.P_Netz_v),
                    (Timestamp, WE14.Wohneinheit, round(WE14.E_bat, 1), round((WE14.E_bat / 3167) * 100, 1), WE14.P_bat_v,WE14.P_load, P_pv, WE14.P_Netz_v),
                    (Timestamp, WE15.Wohneinheit, round(WE15.E_bat, 1), round((WE15.E_bat / 3167) * 100, 1), WE15.P_bat_v,WE15.P_load, P_pv, WE15.P_Netz_v),
                    (Timestamp, WE16.Wohneinheit, round(WE16.E_bat, 1), round((WE16.E_bat / 3167) * 100, 1), WE16.P_bat_v,WE16.P_load, P_pv, WE16.P_Netz_v),
                    (Timestamp, WE17.Wohneinheit, round(WE17.E_bat, 1), round((WE17.E_bat / 3167) * 100, 1), WE17.P_bat_v,WE17.P_load, P_pv, WE17.P_Netz_v),
                    (Timestamp, WE18.Wohneinheit, round(WE18.E_bat, 1), round((WE18.E_bat / 3167) * 100, 1), WE18.P_bat_v,WE18.P_load, P_pv, WE18.P_Netz_v),
                    (Timestamp, WE19.Wohneinheit, round(WE19.E_bat, 1), round((WE19.E_bat / 3167) * 100, 1), WE19.P_bat_v,WE19.P_load, P_pv, WE19.P_Netz_v),
                    (Timestamp, WE20.Wohneinheit, round(WE20.E_bat, 1), round((WE20.E_bat / 3167) * 100, 1), WE20.P_bat_v,WE20.P_load, P_pv, WE20.P_Netz_v),
                    (Timestamp, WE21.Wohneinheit, round(WE21.E_bat, 1), round((WE21.E_bat / 3167) * 100, 1), WE21.P_bat_v,WE21.P_load, P_pv, WE21.P_Netz_v),
                    (Timestamp, WE22.Wohneinheit, round(WE22.E_bat, 1), round((WE22.E_bat / 3167) * 100, 1), WE22.P_bat_v,WE22.P_load, P_pv, WE22.P_Netz_v),
                    (Timestamp, WE23.Wohneinheit, round(WE23.E_bat, 1), round((WE23.E_bat / 3167) * 100, 1), WE23.P_bat_v,WE23.P_load, P_pv, WE23.P_Netz_v),
                    (Timestamp, WE24.Wohneinheit, round(WE24.E_bat, 1), round((WE24.E_bat / 3167) * 100, 1), WE24.P_bat_v,WE24.P_load, P_pv, WE24.P_Netz_v)
                      ]
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute("CREATE TABLE IF NOT EXISTS Tabelle3 "
                      "(Timestamp text, name text PRIMARY KEY,E_bat real, SoC real,P_BSS real, P_Last real,P_PV real, P_Netz real)")
        curSQ.executemany("INSERT OR REPLACE INTO Tabelle3 "
                          "(Timestamp, name, E_bat, SoC,P_BSS, P_Last,P_PV, P_Netz) VALUES (?,?,?,?,?,?,?,?)",(value_list))
        conSQ.commit()
        for row in curSQ.execute("SELECT * FROM Tabelle3"):
            row

    def run(self):
        global P_pv
        global P_bat_real
        global Timestamp_sim
        while True:
            try:
                Wohneinheiten = [WE1, WE2, WE3, WE4, WE5, WE6, WE7, WE8, WE9, WE10, WE11, WE12,
                                 WE13, WE14, WE15, WE16, WE17, WE18, WE19, WE20, WE21, WE22, WE23, WE24]
                for WE in Wohneinheiten:
                    WE.buchen()

                P_bat_real = round(WE1.P_bat_v + WE2.P_bat_v + WE3.P_bat_v + WE4.P_bat_v + WE5.P_bat_v + WE6.P_bat_v + WE7.P_bat_v + WE8.P_bat_v + WE9.P_bat_v + WE10.P_bat_v
                                   + WE11.P_bat_v + WE12.P_bat_v + WE13.P_bat_v + WE14.P_bat_v + WE15.P_bat_v + WE16.P_bat_v + WE17.P_bat_v + WE18.P_bat_v + WE19.P_bat_v + WE20.P_bat_v
                                   + WE21.P_bat_v + WE22.P_bat_v + WE23.P_bat_v + WE24.P_bat_v,1)
                print('Summierte Werte -> P_BSS_sum =',P_bat_real,'W ----------> P_pv_sum =',P_pv*24,'W ----------------> Simulierter Zeitstempel ---',Timestamp_sim)

                self.write_Database()


            except NameError as err:
                #print('NameError -->',str(err))
                pass
            time.sleep(1)

PVabfrage = PVprofil()
Lastabfrage = Lastprofil() #Lastprofil 17 -> Verbrauch 6000 kWh im Jahr
WE1 = Energiekonto('WE1',0,2220,0,0,0.5,0)  #WE,P_bat_r, Energiekonto, betrag,P_load, load_offset
WE2 = Energiekonto('WE2',0,2000,0,0,0.4,0)  #Angabe in Wh
WE3 = Energiekonto('WE3',0,1300,0,0,0.3,0)
WE4 = Energiekonto('WE4',0,1900,0,0,0.35,0)
WE5 = Energiekonto('WE5',0,1000,0,0,0.45,0)
WE6 = Energiekonto('WE6',0,2500,0,0,0.37,0)
WE7 = Energiekonto('WE7',0,1900,0,0,0.29,0)
WE8 = Energiekonto('WE8',0,1000,0,0,0.3,0)
WE9 = Energiekonto('WE9',0,1400,0,0,0.6,0)
WE10 = Energiekonto('WE10',0,1900,0,0,0.55,0)
WE11 = Energiekonto('WE11',0,1000,0,0,0.39,0)
WE12 = Energiekonto('WE12',0,1800,0,0,0.44,0)
WE13 = Energiekonto('WE13',0,1900,0,0,0.3,0)
WE14 = Energiekonto('WE14',0,1000,0,0,0.4,0)
WE15 = Energiekonto('WE15',0,1200,0,0,0.5,0)
WE16 = Energiekonto('WE16',0,1900,0,0,0.25,0)
WE17 = Energiekonto('WE17',0,1000,0,0,0.33,0)
WE18 = Energiekonto('WE18',0,900,0,0,0.45,0)
WE19 = Energiekonto('WE19',0,1900,0,0,0.35,0)
WE20 = Energiekonto('WE20',0,1000,0,0,0.45,0)
WE21 = Energiekonto('WE21',0,1000,0,0,0.35,0)
WE22 = Energiekonto('WE22',0,1100,0,0,0.38,0)
WE23 = Energiekonto('WE23',0,1900,0,0,0.37,0)
WE24 = Energiekonto('WE24',0,1000,0,0,0.39,0)

concurrentthreads = [Lastabfrage,PVabfrage,WE1]
for threads in concurrentthreads:
    threads.start()



# Möglichkeiten für regelmäßige Synchronisation/Kalibrierung ???
#       - Ungenauigkeit durch Verluste
#       - Ungenauigkeit durch sekündliche Energieflussberechnung
#   LÖSUNG: Summierte Werte und Geräte-Auslesewerte regelmäßig gegenüberstellen und Differenz gleichmäßig auf alle WE aufteilen
