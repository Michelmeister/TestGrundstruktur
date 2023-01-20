from threading import Thread
import time
import csv
from datetime import datetime,timezone
import pytz
import sqlite3


class PV_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_pv
        global Timestamp_sim
        P_pv = 0
        Timestamp_sim = 0

        csv_file = open('PV_csv\PV_2021-03-23_06.00.00_to_23.59.59_cloudy.csv',newline='')
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
        P_Last = 0
        csv_file = open('Last_csv\LP17_2010-06-23_06.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile = csv.DictReader(csv_file,delimiter=',')
        for row in load_profile:
            P1 = float(row['P1'])
            P2 = float(row['P2'])
            P3 = float(row['P3'])
            P_Last = P1+P2+P3
            #print(row['Timestamp'],'--->',P_Last,'W')
            time.sleep(1)
class BSS_dummy(Thread):
    def __init__(self):
        super().__init__()
        self.E_bat_device = 25000 # Wh
        self.P_BSS_device = 0 # W # Sollwert für physikalische Lade-/Entladeleistung
        self.delta_E = 0

        self.E_bat_max = 76000 # Wh
        self.E_bat_min = 3800 # Untere Entladegrenze SoC = 5%
        self.SoC = 50
        self.efficiency = 0.85
        self.P_BSS_discharge_max = 65000 # W
        self.P_BSS_charge_max = -65000 #W
        self.Selbstentladung = ((0.03 * 76000)/24)/3600

    def run(self):
        while True:
            time.sleep(1)
            self.P_BSS_device = sum(WE.P_bat_v for WE in Wohneinheiten)
            self.E_bat_device = self.E_bat_device - self.Selbstentladung

            "Physikalische Leistungsbegrenzung BSS"
            if self.P_BSS_device <= self.P_BSS_charge_max:
                self.P_BSS_device = self.P_BSS_charge_max
            elif self.P_BSS_device >= self.P_BSS_discharge_max:
                self.P_BSS_device = self.P_BSS_discharge_max
            else:
                self.P_BSS_device = self.P_BSS_device

            self.delta_E = (-self.P_BSS_device/3600) * self.efficiency

            # "Physikalische Entladegrenze von Soc = 5 - 100% wird in virtueller Aufteilung gesteuert!"
            # if (self.E_bat_device + self.delta_E) >= self.E_bat_max:
            #     self.P_BSS_device = 0
            # elif (self.E_bat_device + self.delta_E) <= self.E_bat_min:
            #     self.P_BSS_device = 0
            # else:
            #     self.P_BSS_device = round(self.P_BSS_device,2)
            #     self.E_bat_device = self.E_bat_device + self.delta_E

            self.P_BSS_device = round(self.P_BSS_device, 2)
            self.E_bat_device = self.E_bat_device + self.delta_E
            self.SoC = round((self.E_bat_device/self.E_bat_max)*100,1)

class MomentanwertDB(Thread):
    def __init__(self):
        super().__init__()

    def Momentanwertdatenbank(self):
        global P_load_sum
        global P_pv_sum
        global Timestamp
        path = 'MomentanwertDB_sim2.db'
        timestamp = datetime.now(timezone.utc)
        local_time= timestamp.astimezone(pytz.timezone('Europe/Berlin'))
        Timestamp = str(local_time.strftime("%d-%m-%Y %H:%M:%S UTC%z"))
        #Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        P_load_sum = round(sum(WE.P_load_v for WE in Wohneinheiten),1)
        P_Netz_sum = round(sum(WE.P_Netz_v for WE in Wohneinheiten),1)
        P_pv_sum = round(sum(WE.P_pv_v for WE in Wohneinheiten),1)
        P_Wallbox_sum = 0
        value_list = [
                    (Timestamp,'Geraetewerte',round(BSS.E_bat_device,2),BSS.SoC,BSS.P_BSS_device,P_load_sum, P_Wallbox_sum,P_pv_sum, P_Netz_sum),
                    (Timestamp,'Rechenwerte',round(WE1.E_bat_sum,2),BSS.SoC,WE1.P_BSS_sum,P_load_sum, P_Wallbox_sum,P_pv_sum, P_Netz_sum),
                    (Timestamp,WE1.Wohneinheit, round(WE1.E_bat_v,2), WE1.SoC_v, WE1.P_bat_v, WE1.P_load_v, WE1.P_Wallbox, WE1.P_pv_v, round(WE1.P_Netz_v,2)),
                    (Timestamp,WE2.Wohneinheit, round(WE2.E_bat_v,2), WE2.SoC_v, WE2.P_bat_v, WE2.P_load_v, WE2.P_Wallbox, WE2.P_pv_v, round(WE2.P_Netz_v,2)),
                    (Timestamp,WE3.Wohneinheit, round(WE3.E_bat_v,2), WE3.SoC_v, WE3.P_bat_v, WE3.P_load_v, WE3.P_Wallbox, WE3.P_pv_v, round(WE3.P_Netz_v,2)),
                    (Timestamp,WE4.Wohneinheit, round(WE4.E_bat_v,2), WE4.SoC_v, WE4.P_bat_v, WE4.P_load_v, WE4.P_Wallbox, WE4.P_pv_v, round(WE4.P_Netz_v,2)),
                    (Timestamp,WE5.Wohneinheit, round(WE5.E_bat_v,2), WE5.SoC_v, WE5.P_bat_v, WE5.P_load_v, WE5.P_Wallbox, WE5.P_pv_v, round(WE5.P_Netz_v,2)),
                    (Timestamp,WE6.Wohneinheit, round(WE6.E_bat_v,2), WE6.SoC_v, WE6.P_bat_v, WE6.P_load_v, WE6.P_Wallbox, WE6.P_pv_v, round(WE6.P_Netz_v,2)),
                    (Timestamp,WE7.Wohneinheit, round(WE7.E_bat_v,2), WE7.SoC_v, WE7.P_bat_v, WE7.P_load_v, WE7.P_Wallbox, WE7.P_pv_v, round(WE7.P_Netz_v,2)),
                    (Timestamp,WE8.Wohneinheit, round(WE8.E_bat_v,2), WE8.SoC_v, WE8.P_bat_v, WE8.P_load_v, WE8.P_Wallbox, WE8.P_pv_v, round(WE8.P_Netz_v,2)),
                    (Timestamp,WE9.Wohneinheit, round(WE9.E_bat_v,2), WE9.SoC_v, WE9.P_bat_v, WE9.P_load_v, WE9.P_Wallbox, WE9.P_pv_v, round(WE9.P_Netz_v,2)),
                    (Timestamp,WE10.Wohneinheit,round(WE10.E_bat_v,2),WE10.SoC_v,WE10.P_bat_v,WE10.P_load_v,WE10.P_Wallbox,WE10.P_pv_v, round(WE10.P_Netz_v,2)),
                    (Timestamp,WE11.Wohneinheit,round(WE11.E_bat_v,2),WE11.SoC_v,WE11.P_bat_v,WE11.P_load_v,WE11.P_Wallbox,WE11.P_pv_v, round(WE11.P_Netz_v,2)),
                    (Timestamp,WE12.Wohneinheit,round(WE12.E_bat_v,2),WE12.SoC_v,WE12.P_bat_v,WE12.P_load_v,WE12.P_Wallbox,WE12.P_pv_v, round(WE12.P_Netz_v,2)),
                    (Timestamp,WE13.Wohneinheit,round(WE13.E_bat_v,2),WE13.SoC_v,WE13.P_bat_v,WE13.P_load_v,WE13.P_Wallbox,WE13.P_pv_v, round(WE13.P_Netz_v,2)),
                    (Timestamp,WE14.Wohneinheit,round(WE14.E_bat_v,2),WE14.SoC_v,WE14.P_bat_v,WE14.P_load_v,WE14.P_Wallbox,WE14.P_pv_v, round(WE14.P_Netz_v,2)),
                    (Timestamp,WE15.Wohneinheit,round(WE15.E_bat_v,2),WE15.SoC_v,WE15.P_bat_v,WE15.P_load_v,WE15.P_Wallbox,WE15.P_pv_v, round(WE15.P_Netz_v,2)),
                    (Timestamp,WE16.Wohneinheit,round(WE16.E_bat_v,2),WE16.SoC_v,WE16.P_bat_v,WE16.P_load_v,WE16.P_Wallbox,WE16.P_pv_v, round(WE16.P_Netz_v,2)),
                    (Timestamp,WE17.Wohneinheit,round(WE17.E_bat_v,2),WE17.SoC_v,WE17.P_bat_v,WE17.P_load_v,WE17.P_Wallbox,WE17.P_pv_v, round(WE17.P_Netz_v,2)),
                    (Timestamp,WE18.Wohneinheit,round(WE18.E_bat_v,2),WE18.SoC_v,WE18.P_bat_v,WE18.P_load_v,WE18.P_Wallbox,WE18.P_pv_v, round(WE18.P_Netz_v,2)),
                    (Timestamp,WE19.Wohneinheit,round(WE19.E_bat_v,2),WE19.SoC_v,WE19.P_bat_v,WE19.P_load_v,WE19.P_Wallbox,WE19.P_pv_v, round(WE19.P_Netz_v,2)),
                    (Timestamp,WE20.Wohneinheit,round(WE20.E_bat_v,2),WE20.SoC_v,WE20.P_bat_v,WE20.P_load_v,WE20.P_Wallbox,WE20.P_pv_v, round(WE20.P_Netz_v,2)),
                    (Timestamp,WE21.Wohneinheit,round(WE21.E_bat_v,2),WE21.SoC_v,WE21.P_bat_v,WE21.P_load_v,WE21.P_Wallbox,WE21.P_pv_v, round(WE21.P_Netz_v,2)),
                    (Timestamp,WE22.Wohneinheit,round(WE22.E_bat_v,2),WE22.SoC_v,WE22.P_bat_v,WE22.P_load_v,WE22.P_Wallbox,WE22.P_pv_v, round(WE22.P_Netz_v,2)),
                    (Timestamp,WE23.Wohneinheit,round(WE23.E_bat_v,2),WE23.SoC_v,WE23.P_bat_v,WE23.P_load_v,WE23.P_Wallbox,WE23.P_pv_v, round(WE23.P_Netz_v,2)),
                    (Timestamp,WE24.Wohneinheit,round(WE24.E_bat_v,2),WE24.SoC_v,WE24.P_bat_v,WE24.P_load_v,WE24.P_Wallbox,WE24.P_pv_v, round(WE24.P_Netz_v,2))
                      ]
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute("CREATE TABLE IF NOT EXISTS Tabelle2 "
                      "(Timestamp text, Name text PRIMARY KEY,E_BSS real, SoC real,P_BSS real, P_Last real, P_Wallbox real,P_PV real, P_Netz real)")
        curSQ.executemany("INSERT OR REPLACE INTO Tabelle2 "
                          "(Timestamp, Name, E_BSS, SoC,P_BSS, P_Last, P_Wallbox,P_PV, P_Netz) VALUES (?,?,?,?,?,?,?,?,?)",(value_list))
        conSQ.commit()
        for row in curSQ.execute("SELECT * FROM Tabelle2"):
            row

    def run(self):
        while True:
            Momentanwerte.Momentanwertdatenbank()
            time.sleep(2)
class ZeitreihenDB(Thread):
    def __init__(self):
        super().__init__()

    def CSV_Daten(self):
        global P_load_sum
        global P_pv_sum
        time = datetime.now()
        csv_name = str(time.strftime("%d%b%Y"))
        timestamp = datetime.now(timezone.utc)
        local_time= timestamp.astimezone(pytz.timezone('Europe/Berlin'))
        Timestamp = str(local_time.strftime("%d-%m-%Y %H:%M:%S UTC%z"))

        path2 = 'ZeitreihenDB\data_' + csv_name + '.db'

        csv_list_we1 = [Timestamp, round(WE1.E_bat_v,2), WE1.SoC_v,WE1.P_bat_v,WE1.P_load_v,WE1.P_Wallbox,WE1.P_pv_v,round(WE1.P_Netz_v,2)]
        csv_list_we2 = [Timestamp, round(WE2.E_bat_v,2), WE2.SoC_v,WE2.P_bat_v,WE2.P_load_v,WE2.P_Wallbox,WE2.P_pv_v,round(WE2.P_Netz_v,2)]
        #csv_list_we3 = [time, round(WE3.E_bat_v,2), WE3.SoC_v,WE3.P_bat_v,WE3.P_load_v,WE3.P_Wallbox,WE3.P_pv_v,WE3.P_Netz_v]

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
            time.sleep(0.9)
            Zeitreihe.CSV_Daten()
class Handelstabelle(Thread):
    def __init__(self):
        super().__init__()

    def read_Handelsstatus(self):
        conn = sqlite3.connect('marketDB_sim.db')
        cc = conn.cursor()
        cc.execute('SELECT * FROM MarktTabelle')
        value = cc.fetchall()

        WE1.PV_Handelsstatus = value[1][1]
        WE2.PV_Handelsstatus = value[2][1]
        WE3.PV_Handelsstatus = value[3][1]
        WE4.PV_Handelsstatus = value[4][1]
        WE5.PV_Handelsstatus = value[5][1]
        WE6.PV_Handelsstatus = value[6][1]
        WE7.PV_Handelsstatus = value[7][1]
        WE8.PV_Handelsstatus = value[8][1]
        WE9.PV_Handelsstatus = value[9][1]
        WE10.PV_Handelsstatus = value[10][1]
        WE11.PV_Handelsstatus = value[11][1]
        WE12.PV_Handelsstatus = value[12][1]
        WE13.PV_Handelsstatus = value[13][1]
        WE14.PV_Handelsstatus = value[14][1]
        WE15.PV_Handelsstatus = value[15][1]
        WE16.PV_Handelsstatus = value[16][1]
        WE17.PV_Handelsstatus = value[17][1]
        WE18.PV_Handelsstatus = value[18][1]
        WE19.PV_Handelsstatus = value[19][1]
        WE20.PV_Handelsstatus = value[20][1]
        WE21.PV_Handelsstatus = value[21][1]
        WE22.PV_Handelsstatus = value[22][1]
        WE23.PV_Handelsstatus = value[23][1]
        WE24.PV_Handelsstatus = value[24][1]

    def run(self):
        while True:
            time.sleep(0.9)
            Handel.read_Handelsstatus()
            #print(WE4.PV_Handelsstatus)

class BSS_virtuell(Thread):
    def __init__(self,Wohneinheit,load_offset):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.P_bat_v = 0
        self.E_bat_v = (BSS.E_bat_device/24)
        self.E_bat_v_max = 3167
        self.E_bat_v_min = 158
        self.E_bat_sum = 35000 # initial value
        self.P_BSS_sum = 0
        self.Selbstentladung_v = (BSS.Selbstentladung/24)
        self.dE_v = 0
        self.P_load_v = 0
        self.load_offset = load_offset
        self.P_Netz_v = 0
        self.SoC_v = 50
        self.P_Wallbox = 0
        self.P_pv_v = 0
        self.PV_Handelsstatus = 0

    def Energiehandel(self):

        if self.PV_Handelsstatus == 'PV_F0':
            self.P_pv_v = 0
        elif self.PV_Handelsstatus == 'PV_F2':
            self.P_pv_v = P_pv * 2
        elif self.PV_Handelsstatus == 'PV_F3':
            self.P_pv_v = P_pv * 3
        elif self.PV_Handelsstatus == 'PV_F4':
            self.P_pv_v = P_pv * 4
        elif self.PV_Handelsstatus == 'PV_F5':
            self.P_pv_v = P_pv * 5
        elif self.PV_Handelsstatus == 'PV_F6':
            self.P_pv_v = P_pv * 6
        elif self.PV_Handelsstatus == 'PV_F7':
            self.P_pv_v = P_pv * 7
        elif self.PV_Handelsstatus == 'PV_F8':
            self.P_pv_v = P_pv * 8
        else:
            self.P_pv_v = P_pv
            # == PV_F1


    def strategy1_ueberschussladen(self):
        self.P_load_v = (P_Last * self.load_offset)
        self.E_bat_v = self.E_bat_v - self.Selbstentladung_v
        self.dE_v = (-self.P_load_v + self.P_pv_v) * (1/3600) * BSS.efficiency
        self.SoC_v = round(((self.E_bat_v/self.E_bat_v_max)*100),1)

        # if self.E_bat_v + self.dE_v <= self.E_bat_v_min:
        #     #print('Energiekonto von',self.Wohneinheit,'leer, setze Entladeleistung P_bat = 0')
        #     'Tiefenentladungsschutz: Physikalischer SoC wird auf 5% gehalten'
        #     if BSS.E_bat_device <= BSS.E_bat_min:
        #         self.P_bat_v = -100
        #         self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v
        #         self.E_bat_v = self.E_bat_v + ((-self.P_bat_v / 3600) * BSS.efficiency)
        #     else:
        #         self.P_bat_v = 0
        #         self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        if BSS.E_bat_device <= BSS.E_bat_min:
            'Tiefenentladungsschutz, phy. Bat kann niemals unter SoC = 5%'
            self.P_bat_v = -100 - self.P_pv_v
            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.P_Netz_v = self.P_load_v - self.P_bat_v
            self.E_bat_v = self.E_bat_v + self.dE_v
        elif self.E_bat_v <= self.E_bat_v_min:
            self.P_bat_v = 0 - self.P_pv_v
            self.P_Netz_v = self.P_load_v
            self.dE_v = (-self.P_bat_v / 3600) * BSS.efficiency
            self.E_bat_v = self.E_bat_v + self.dE_v

        elif self.E_bat_v + self.dE_v >= self.E_bat_v_max:  #SoC=100%
            #print('Energiekonto von',self.Wohneinheit, 'ist voll, setze Ladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        else:
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_bat_v = round(self.P_load_v - self.P_pv_v,2)       # bei PV-Überschuss negativer Wert -> Speicher laden!
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        self.E_bat_sum = round(sum(WE.E_bat_v for WE in Wohneinheiten),1)
        self.P_BSS_sum = round(sum(WE.P_bat_v for WE in Wohneinheiten),1)


    def run(self):  # AUFRUF DER BETRIEBSSTRATEGIE
        print('EMS in Ausführung!')
        while True:
            try:
                for WE in Wohneinheiten:
                    WE.Energiehandel()
                    WE.strategy1_ueberschussladen()

                #print('Summierte Werte -> P_BSS_sum =',WE1.P_BSS_sum,'W ---> P_load_sum =',P_load_sum,'W ---> P_pv_sum =',P_pv_sum,'W ---> Simulierter Zeitstempel ---',Timestamp_sim)
                #print('Kontrollrechnung --> WE 1: E_bat =',round(WE1.E_bat_v,4),'Wh --> P_BSS_v =',WE1.P_bat_v,'W --> dE =',WE1.dE_v,'Wh')
                print('Simulierter Zeitstempel ->',Timestamp_sim)

            except NameError as err:
                print('NameError --->',str(err))

            time.sleep(1)



BSS = BSS_dummy()
PV = PV_dummy()
Last = Last_dummy()
Momentanwerte = MomentanwertDB()
Zeitreihe = ZeitreihenDB()
Handel = Handelstabelle()

WE1 = BSS_virtuell('WE1',0.7)  #WE, E_bat_v, load_offset
WE2 = BSS_virtuell('WE2',0.4)
WE3 = BSS_virtuell('WE3',0.3)
WE4 = BSS_virtuell('WE4',0.35)
WE5 = BSS_virtuell('WE5',0.45)
WE6 = BSS_virtuell('WE6',0.37)
WE7 = BSS_virtuell('WE7',0.29)
WE8 = BSS_virtuell('WE8',0.3)
WE9 = BSS_virtuell('WE9',0.6)
WE10 = BSS_virtuell('WE10',0.55)
WE11 = BSS_virtuell('WE11',0.39)
WE12 = BSS_virtuell('WE12',1.0)
WE13 = BSS_virtuell('WE13',0.3)
WE14 = BSS_virtuell('WE14',0.5)
WE15 = BSS_virtuell('WE15',0.5)
WE16 = BSS_virtuell('WE16',0.25)
WE17 = BSS_virtuell('WE17',0.33)
WE18 = BSS_virtuell('WE18',0.45)
WE19 = BSS_virtuell('WE19',0.35)
WE20 = BSS_virtuell('WE20',0.45)
WE21 = BSS_virtuell('WE21',0.35)
WE22 = BSS_virtuell('WE22',0.38)
WE23 = BSS_virtuell('WE23',0.37)
WE24 = BSS_virtuell('WE24',0.39)
Wohneinheiten = [WE1, WE2, WE3, WE4, WE5, WE6, WE7, WE8, WE9, WE10, WE11, WE12,
                 WE13, WE14, WE15, WE16, WE17, WE18, WE19, WE20, WE21, WE22, WE23, WE24]


concurrentthreads = [PV,Last,BSS,Momentanwerte,WE1,Handel] #Zeitreihe]
for threads in concurrentthreads:
    threads.start()
