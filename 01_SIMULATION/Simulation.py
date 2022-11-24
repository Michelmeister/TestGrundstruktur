from threading import Thread
import time
import csv
import datetime
import sqlite3


class PV_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_pv
        global Timestamp_sim

        csv_file = open('PV_csv\PV_2021-03-23_18.00.00_to_23.59.59_cloudy.csv',newline='')
        pv_profile = csv.DictReader(csv_file,delimiter=',')
        for row in pv_profile:
            if row['P_TOTAL'] == '':
                pass
            else:
                P_tot = float(row['P_TOTAL'])
                P_pv = round((2/7) * P_tot) # W
                #print(P_pv)
            Timestamp_sim = (row['Timestamp'])
            time.sleep(1)
class Last_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_Last
        csv_file = open('Last_csv\LP17_2010-06-23_18.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile = csv.DictReader(csv_file,delimiter=',')
        for row in load_profile:
            P1 = float(row['P1'])
            P2 = float(row['P2'])
            P3 = float(row['P3'])
            P_Last = P1+P2+P3
            #print(row['Timestamp'],'--->',P_Last,'W')
            time.sleep(1)
class BSS_dummy(Thread):
    def __init__(self,E_bat_sum,E_bat_max,P_BSS_sum, SoC):
        super().__init__()
        self.E_bat_sum = E_bat_sum
        self.E_bat_max = E_bat_max
        self.P_BSS_sum = P_BSS_sum
        self.SoC = SoC

    def run(self):
        while True:
            time.sleep(1)
            self.SoC = round((self.E_bat_sum/self.E_bat_max)*100,1)
            self.E_bat_sum = round(sum(WE.E_bat_v for WE in Wohneinheiten),2)
            self.P_BSS_sum = round(sum(WE.P_bat_v for WE in Wohneinheiten),1)
class Database(Thread):
    def __init__(self):
        super().__init__()

    def Momentanwertdatenbank(self):
        global P_pv
        global P_Last
        global P_load_sum
        path = 'MomentanwertDB_sim2.db'
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        P_load_sum = round(sum(WE.P_load_v for WE in Wohneinheiten),1)
        P_Netz_sum = round(sum(WE.P_Netz_v for WE in Wohneinheiten),1)
        P_pv_sum = round(sum(WE.P_pv_v for WE in Wohneinheiten),1)
        P_Wallbox_sum = 0
        value_list = [
                    (Timestamp,'Geraetewerte',BSS.E_bat_sum,BSS.SoC,BSS.P_BSS_sum,P_load_sum, P_Wallbox_sum,P_pv_sum, P_Netz_sum),
                    (Timestamp,WE1.Wohneinheit, WE1.E_bat_v, WE1.SoC_v, WE1.P_bat_v, WE1.P_load_v, WE1.P_Wallbox, WE1.P_pv_v, WE1.P_Netz_v),
                    (Timestamp,WE2.Wohneinheit, WE2.E_bat_v, WE2.SoC_v, WE2.P_bat_v, WE2.P_load_v, WE2.P_Wallbox, WE2.P_pv_v, WE2.P_Netz_v),
                    (Timestamp,WE3.Wohneinheit, WE3.E_bat_v, WE3.SoC_v, WE3.P_bat_v, WE3.P_load_v, WE3.P_Wallbox, WE3.P_pv_v, WE3.P_Netz_v),
                    (Timestamp,WE4.Wohneinheit, WE4.E_bat_v, WE4.SoC_v, WE4.P_bat_v, WE4.P_load_v, WE4.P_Wallbox, WE4.P_pv_v, WE4.P_Netz_v),
                    (Timestamp,WE5.Wohneinheit, WE5.E_bat_v, WE5.SoC_v, WE5.P_bat_v, WE5.P_load_v, WE5.P_Wallbox, WE5.P_pv_v, WE5.P_Netz_v),
                    (Timestamp,WE6.Wohneinheit, WE6.E_bat_v, WE6.SoC_v, WE6.P_bat_v, WE6.P_load_v, WE6.P_Wallbox, WE6.P_pv_v, WE6.P_Netz_v),
                    (Timestamp,WE7.Wohneinheit, WE7.E_bat_v, WE7.SoC_v, WE7.P_bat_v, WE7.P_load_v, WE7.P_Wallbox, WE7.P_pv_v, WE7.P_Netz_v),
                    (Timestamp,WE8.Wohneinheit, WE8.E_bat_v, WE8.SoC_v, WE8.P_bat_v, WE8.P_load_v, WE8.P_Wallbox, WE8.P_pv_v, WE8.P_Netz_v),
                    (Timestamp,WE9.Wohneinheit, WE9.E_bat_v, WE9.SoC_v, WE9.P_bat_v, WE9.P_load_v, WE9.P_Wallbox, WE9.P_pv_v, WE9.P_Netz_v),
                    (Timestamp,WE10.Wohneinheit,WE10.E_bat_v,WE10.SoC_v,WE10.P_bat_v,WE10.P_load_v,WE10.P_Wallbox,WE10.P_pv_v, WE10.P_Netz_v),
                    (Timestamp,WE11.Wohneinheit,WE11.E_bat_v,WE11.SoC_v,WE11.P_bat_v,WE11.P_load_v,WE11.P_Wallbox,WE11.P_pv_v, WE11.P_Netz_v),
                    (Timestamp,WE12.Wohneinheit,WE12.E_bat_v,WE12.SoC_v,WE12.P_bat_v,WE12.P_load_v,WE12.P_Wallbox,WE12.P_pv_v, WE12.P_Netz_v),
                    (Timestamp,WE13.Wohneinheit,WE13.E_bat_v,WE13.SoC_v,WE13.P_bat_v,WE13.P_load_v,WE13.P_Wallbox,WE13.P_pv_v, WE13.P_Netz_v),
                    (Timestamp,WE14.Wohneinheit,WE14.E_bat_v,WE14.SoC_v,WE14.P_bat_v,WE14.P_load_v,WE14.P_Wallbox,WE14.P_pv_v, WE14.P_Netz_v),
                    (Timestamp,WE15.Wohneinheit,WE15.E_bat_v,WE15.SoC_v,WE15.P_bat_v,WE15.P_load_v,WE15.P_Wallbox,WE15.P_pv_v, WE15.P_Netz_v),
                    (Timestamp,WE16.Wohneinheit,WE16.E_bat_v,WE16.SoC_v,WE16.P_bat_v,WE16.P_load_v,WE16.P_Wallbox,WE16.P_pv_v, WE16.P_Netz_v),
                    (Timestamp,WE17.Wohneinheit,WE17.E_bat_v,WE17.SoC_v,WE17.P_bat_v,WE17.P_load_v,WE17.P_Wallbox,WE17.P_pv_v, WE17.P_Netz_v),
                    (Timestamp,WE18.Wohneinheit,WE18.E_bat_v,WE18.SoC_v,WE18.P_bat_v,WE18.P_load_v,WE18.P_Wallbox,WE18.P_pv_v, WE18.P_Netz_v),
                    (Timestamp,WE19.Wohneinheit,WE19.E_bat_v,WE19.SoC_v,WE19.P_bat_v,WE19.P_load_v,WE19.P_Wallbox,WE19.P_pv_v, WE19.P_Netz_v),
                    (Timestamp,WE20.Wohneinheit,WE20.E_bat_v,WE20.SoC_v,WE20.P_bat_v,WE20.P_load_v,WE20.P_Wallbox,WE20.P_pv_v, WE20.P_Netz_v),
                    (Timestamp,WE21.Wohneinheit,WE21.E_bat_v,WE21.SoC_v,WE21.P_bat_v,WE21.P_load_v,WE21.P_Wallbox,WE21.P_pv_v, WE21.P_Netz_v),
                    (Timestamp,WE22.Wohneinheit,WE22.E_bat_v,WE22.SoC_v,WE22.P_bat_v,WE22.P_load_v,WE22.P_Wallbox,WE22.P_pv_v, WE22.P_Netz_v),
                    (Timestamp,WE23.Wohneinheit,WE23.E_bat_v,WE23.SoC_v,WE23.P_bat_v,WE23.P_load_v,WE23.P_Wallbox,WE23.P_pv_v, WE23.P_Netz_v),
                    (Timestamp,WE24.Wohneinheit,WE24.E_bat_v,WE24.SoC_v,WE24.P_bat_v,WE24.P_load_v,WE24.P_Wallbox,WE24.P_pv_v, WE24.P_Netz_v)
                      ]
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute("CREATE TABLE IF NOT EXISTS Tabelle1 "
                      "(Timestamp text, name text PRIMARY KEY,E_bat real, SoC real,P_BSS real, P_Last real, P_Wallbox real,P_PV real, P_Netz real)")
        curSQ.executemany("INSERT OR REPLACE INTO Tabelle1 "
                          "(Timestamp, name, E_bat, SoC,P_BSS, P_Last, P_Wallbox,P_PV, P_Netz) VALUES (?,?,?,?,?,?,?,?,?)",(value_list))
        conSQ.commit()
        for row in curSQ.execute("SELECT * FROM Tabelle1"):
            row

    def CSV_Daten(self):
        global P_pv
        timestamp = datetime.datetime.now()
        Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        month = str(timestamp.strftime("%b%Y"))

        path2 = 'CSV_Datenbank\data_' + month + '_sim1.db'

        csv_list_we1 = [Timestamp, WE1.E_bat_v, WE1.SoC_v,WE1.P_bat_v,WE1.P_load_v,WE1.P_Wallbox,WE1.P_pv_v,WE1.P_Netz_v]
        csv_list_we2 = [Timestamp, WE2.E_bat_v, WE2.SoC_v,WE2.P_bat_v,WE2.P_load_v,WE2.P_Wallbox,WE2.P_pv_v,WE2.P_Netz_v]
        csv_list_we3 = [Timestamp, WE3.E_bat_v, WE3.SoC_v,WE3.P_bat_v,WE3.P_load_v,WE3.P_Wallbox,WE3.P_pv_v,WE3.P_Netz_v]

        connectSQ = sqlite3.connect(path2)
        cursorSQ = connectSQ.cursor()
        cursorSQ.execute("CREATE TABLE IF NOT EXISTS WE1_sim1 "
                      "(Timestamp text PRIMARY KEY ,E_Bat real, SoC real,P_BSS real,P_Last real, P_Wallbox real, P_pv real,P_Netz real)")
        cursorSQ.execute("CREATE TABLE IF NOT EXISTS WE2_sim1 "
                      "(Timestamp text PRIMARY KEY ,E_Bat real, SoC real,P_BSS real,P_Last real, P_Wallbox real, P_pv real,P_Netz real)")


        cursorSQ.execute("INSERT OR IGNORE INTO WE1_sim1 "
                          "(Timestamp ,E_Bat, SoC,P_BSS,P_Last, P_Wallbox, P_pv,P_Netz) VALUES (?,?,?,?,?,?,?,?)",(csv_list_we1))
        cursorSQ.execute("INSERT OR IGNORE INTO WE2_sim1 "
                          "(Timestamp ,E_Bat, SoC,P_BSS,P_Last, P_Wallbox, P_pv,P_Netz) VALUES (?,?,?,?,?,?,?,?)",(csv_list_we2))

        connectSQ.commit()
        for row in cursorSQ.execute("SELECT * FROM WE1_sim1"):
            row
        for row in cursorSQ.execute("SELECT * FROM WE2_sim1"):
            row

    def run(self):
        while True:
            data.Momentanwertdatenbank()
            data.CSV_Daten()



class BSS_virtuell(Thread):
    def __init__(self,Wohneinheit,P_bat_v,E_bat_v,dE_v,P_load_v,load_offset,P_Netz_v,SoC_v, E_bat_v_max,P_Wallbox,P_pv_v):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.P_bat_v = P_bat_v
        self.E_bat_v = E_bat_v
        self.dE_v = dE_v
        self.P_load_v = P_load_v
        self.load_offset = load_offset
        self.P_Netz_v = P_Netz_v
        self.SoC_v = SoC_v
        self.E_bat_v_max = E_bat_v_max
        self.P_Wallbox = P_Wallbox
        self.P_pv_v = P_pv_v

    def strategy1_ueberschussladen(self):
        global P_Last
        global P_pv

        self.P_load_v = P_Last*self.load_offset
        self.P_pv_v = P_pv
        self.dE_v = (-self.P_load_v * (1/3600)) + (P_pv * (1/3600))
        self.SoC_v = round(((self.E_bat_v/self.E_bat_v_max)*100),1)

        if self.E_bat_v + self.dE_v <= 158:     #SoC=5%
            #print('Energiekonto von',self.Wohneinheit,'leer, setze Entladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - P_pv - self.P_bat_v


        elif self.E_bat_v + self.dE_v >= 3167:
            #print('Energiekonto von',self.Wohneinheit, 'ist voll, setze Ladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - P_pv - self.P_bat_v

        else:
            self.E_bat_v = round((self.E_bat_v + self.dE_v) ,2)
            self.P_bat_v = self.P_load_v - P_pv       # bei PV-Überschuss negativer Wert -> Speicher laden!
            self.P_Netz_v = self.P_load_v - P_pv - self.P_bat_v


    def run(self):  # AUFRUF DER BETRIEBSSTRATEGIE
        global P_pv
        global Timestamp_sim
        global P_load_sum
        a = 1
        while True:
            for WE in Wohneinheiten:
                if a == 1: # Hier können später Bedingungen gesetzt werden, wann welche Strategie gefahren werden soll
                    WE.strategy1_ueberschussladen()
                else:
                    WE.strategy1_ueberschussladen()
                    pass

            print('Summierte Werte -> P_BSS_sum =',BSS.P_BSS_sum,'W ---> P_load_sum =',P_load_sum,'W ---> P_pv_sum =',P_pv*24,'W ---> Simulierter Zeitstempel ---',Timestamp_sim)
            time.sleep(1)



BSS = BSS_dummy(7600,76000,0,50) #E_bat_sum, E_bat_max, P_BSS_sum, SoC
PV = PV_dummy()
Last = Last_dummy()
data = Database()

WE1 = BSS_virtuell('WE1',0,2220,0,0,0.5,0,20,3167,0,0)  #WE,P_bat_v, E_bat_v, dE_v,P_load_v, load_offset, P_Netz, SoC_v, E_bat_v_max, P_Wallbox,P_pv_v
WE2 = BSS_virtuell('WE2',0,2000,0,0,0.4,0,20,3167,0,0)  #Angabe in W bzw. Wh
WE3 = BSS_virtuell('WE3',0,1300,0,0,0.3,0,20,3167,0,0)
WE4 = BSS_virtuell('WE4',0,1900,0,0,0.35,0,20,3167,0,0)
WE5 = BSS_virtuell('WE5',0,1000,0,0,0.45,0,20,3167,0,0)
WE6 = BSS_virtuell('WE6',0,2500,0,0,0.37,0,20,3167,0,0)
WE7 = BSS_virtuell('WE7',0,1900,0,0,0.29,0,20,3167,0,0)
WE8 = BSS_virtuell('WE8',0,1000,0,0,0.3,0,20,3167,0,0)
WE9 = BSS_virtuell('WE9',0,1400,0,0,0.6,0,20,3167,0,0)
WE10 = BSS_virtuell('WE10',0,1900,0,0,0.55,0,20,3167,0,0)
WE11 = BSS_virtuell('WE11',0,1000,0,0,0.39,0,20,3167,0,0)
WE12 = BSS_virtuell('WE12',0,1800,0,0,0.44,0,20,3167,0,0)
WE13 = BSS_virtuell('WE13',0,1900,0,0,0.3,0,20,3167,0,0)
WE14 = BSS_virtuell('WE14',0,1000,0,0,0.4,0,20,3167,0,0)
WE15 = BSS_virtuell('WE15',0,1200,0,0,0.5,0,20,3167,0,0)
WE16 = BSS_virtuell('WE16',0,1900,0,0,0.25,0,20,3167,0,0)
WE17 = BSS_virtuell('WE17',0,1000,0,0,0.33,0,20,3167,0,0)
WE18 = BSS_virtuell('WE18',0,900,0,0,0.45,0,20,3167,0,0)
WE19 = BSS_virtuell('WE19',0,1900,0,0,0.35,0,20,3167,0,0)
WE20 = BSS_virtuell('WE20',0,1000,0,0,0.45,0,20,3167,0,0)
WE21 = BSS_virtuell('WE21',0,1000,0,0,0.35,0,20,3167,0,0)
WE22 = BSS_virtuell('WE22',0,1100,0,0,0.38,0,20,3167,0,0)
WE23 = BSS_virtuell('WE23',0,1900,0,0,0.37,0,20,3167,0,0)
WE24 = BSS_virtuell('WE24',0,1000,0,0,0.39,0,20,3167,0,0)
Wohneinheiten = [WE1, WE2, WE3, WE4, WE5, WE6, WE7, WE8, WE9, WE10, WE11, WE12,
                 WE13, WE14, WE15, WE16, WE17, WE18, WE19, WE20, WE21, WE22, WE23, WE24]



concurrentthreads = [PV,Last,BSS,data,WE1]
for threads in concurrentthreads:
    threads.start()