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

        csv_file = open('PV_csv\PV_2021-06-24_12.00.00_to_23.59.59_cloudy.csv',newline='')
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
        csv_file = open('Last_csv\LP17_2010-06-23_12.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile = csv.DictReader(csv_file,delimiter=',')
        for row in load_profile:
            P1 = float(row['P1'])
            P2 = float(row['P2'])
            P3 = float(row['P3'])
            P_Last = (P1+P2+P3)
            #print(row['Timestamp'],'--->',P_Last,'W')
            time.sleep(1)
class EV_charging_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_EV
        P_EV = 0
        csv_EVfile = open('EV_csv/2020-01-06_Monday.csv',newline='')
        EV_profile = csv.DictReader(csv_EVfile,delimiter=',')
        for row in EV_profile:
            P1 = float(row['Load_kW'])
            #print(row['Timestamp'],'--->',P_Last,'W')
            time.sleep(1)

class BSS_dummy(Thread):
    def __init__(self):
        super().__init__()
        self.E_bat_device = 38000 # Wh
        self.P_BSS_device = 0 # W # Sollwert für physikalische Lade-/Entladeleistung
        self.delta_E = 0

        self.E_bat_max = 67000 # Wh
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

            # "Physikalische Leistungsbegrenzung BSS"
            # if self.P_BSS_device <= self.P_BSS_charge_max:
            #     self.P_BSS_device = self.P_BSS_charge_max
            # elif self.P_BSS_device >= self.P_BSS_discharge_max:
            #     self.P_BSS_device = self.P_BSS_discharge_max
            # else:
            #     self.P_BSS_device = self.P_BSS_device

            self.delta_E = (-self.P_BSS_device/3600) * self.efficiency

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

        csv_list_we1 = [Timestamp, round(WE1.E_bat_v,2), WE1.SoC_v, WE1.P_bat_v, WE1.P_load_v, WE1.P_Wallbox, WE1.P_pv_v, round(WE1.P_Netz_v,2)]
        csv_list_we2 = [Timestamp, round(WE2.E_bat_v,2), WE2.SoC_v, WE2.P_bat_v, WE2.P_load_v, WE2.P_Wallbox, WE2.P_pv_v, round(WE2.P_Netz_v,2)]
        csv_list_we3 = [Timestamp, round(WE3.E_bat_v,2), WE3.SoC_v, WE3.P_bat_v, WE3.P_load_v, WE3.P_Wallbox, WE3.P_pv_v, round(WE3.P_Netz_v,2)]
        csv_list_we4 = [Timestamp, round(WE4.E_bat_v,2), WE4.SoC_v, WE4.P_bat_v, WE4.P_load_v, WE4.P_Wallbox, WE4.P_pv_v, round(WE4.P_Netz_v,2)]
        csv_list_we5 = [Timestamp, round(WE5.E_bat_v,2), WE5.SoC_v, WE5.P_bat_v, WE5.P_load_v, WE5.P_Wallbox, WE5.P_pv_v, round(WE5.P_Netz_v,2)]
        csv_list_we6 = [Timestamp, round(WE6.E_bat_v,2), WE6.SoC_v, WE6.P_bat_v, WE6.P_load_v, WE6.P_Wallbox, WE6.P_pv_v, round(WE6.P_Netz_v,2)]
        csv_list_we7 = [Timestamp, round(WE7.E_bat_v,2), WE7.SoC_v, WE7.P_bat_v, WE7.P_load_v, WE7.P_Wallbox, WE7.P_pv_v, round(WE7.P_Netz_v,2)]
        csv_list_we8 = [Timestamp, round(WE8.E_bat_v,2), WE8.SoC_v, WE8.P_bat_v, WE8.P_load_v, WE8.P_Wallbox, WE8.P_pv_v, round(WE8.P_Netz_v,2)]
        csv_list_we9 = [Timestamp, round(WE9.E_bat_v,2), WE9.SoC_v, WE9.P_bat_v, WE9.P_load_v, WE9.P_Wallbox, WE9.P_pv_v, round(WE9.P_Netz_v,2)]
        csv_list_we10 = [Timestamp, round(WE10.E_bat_v,2), WE10.SoC_v, WE10.P_bat_v, WE10.P_load_v, WE10.P_Wallbox, WE10.P_pv_v, round(WE10.P_Netz_v,2)]
        csv_list_we11 = [Timestamp, round(WE11.E_bat_v,2), WE11.SoC_v, WE11.P_bat_v, WE11.P_load_v, WE11.P_Wallbox, WE11.P_pv_v, round(WE11.P_Netz_v,2)]
        csv_list_we12 = [Timestamp, round(WE12.E_bat_v,2), WE12.SoC_v, WE12.P_bat_v, WE12.P_load_v, WE12.P_Wallbox, WE12.P_pv_v, round(WE12.P_Netz_v,2)]
        csv_list_we13 = [Timestamp, round(WE13.E_bat_v,2), WE13.SoC_v, WE13.P_bat_v, WE13.P_load_v, WE13.P_Wallbox, WE13.P_pv_v, round(WE13.P_Netz_v,2)]
        csv_list_we14 = [Timestamp, round(WE14.E_bat_v,2), WE14.SoC_v, WE14.P_bat_v, WE14.P_load_v, WE14.P_Wallbox, WE14.P_pv_v, round(WE14.P_Netz_v,2)]
        csv_list_we15 = [Timestamp, round(WE15.E_bat_v,2), WE15.SoC_v, WE15.P_bat_v, WE15.P_load_v, WE15.P_Wallbox, WE15.P_pv_v, round(WE15.P_Netz_v,2)]
        csv_list_we16 = [Timestamp, round(WE16.E_bat_v,2), WE16.SoC_v, WE16.P_bat_v, WE16.P_load_v, WE16.P_Wallbox, WE16.P_pv_v, round(WE16.P_Netz_v,2)]
        csv_list_we17 = [Timestamp, round(WE17.E_bat_v,2), WE17.SoC_v, WE17.P_bat_v, WE17.P_load_v, WE17.P_Wallbox, WE17.P_pv_v, round(WE17.P_Netz_v,2)]
        csv_list_we18 = [Timestamp, round(WE18.E_bat_v,2), WE18.SoC_v, WE18.P_bat_v, WE18.P_load_v, WE18.P_Wallbox, WE18.P_pv_v, round(WE18.P_Netz_v,2)]
        csv_list_we19 = [Timestamp, round(WE19.E_bat_v,2), WE19.SoC_v, WE19.P_bat_v, WE19.P_load_v, WE19.P_Wallbox, WE19.P_pv_v, round(WE19.P_Netz_v,2)]
        csv_list_we20 = [Timestamp, round(WE20.E_bat_v,2), WE20.SoC_v, WE20.P_bat_v, WE20.P_load_v, WE20.P_Wallbox, WE20.P_pv_v, round(WE20.P_Netz_v,2)]
        csv_list_we21 = [Timestamp, round(WE21.E_bat_v,2), WE21.SoC_v, WE21.P_bat_v, WE21.P_load_v, WE21.P_Wallbox, WE21.P_pv_v, round(WE21.P_Netz_v,2)]
        csv_list_we22 = [Timestamp, round(WE22.E_bat_v,2), WE22.SoC_v, WE22.P_bat_v, WE22.P_load_v, WE22.P_Wallbox, WE22.P_pv_v, round(WE22.P_Netz_v,2)]
        csv_list_we23 = [Timestamp, round(WE23.E_bat_v,2), WE23.SoC_v, WE23.P_bat_v, WE23.P_load_v, WE23.P_Wallbox, WE23.P_pv_v, round(WE23.P_Netz_v,2)]
        csv_list_we24 = [Timestamp, round(WE24.E_bat_v,2), WE24.SoC_v, WE24.P_bat_v, WE24.P_load_v, WE24.P_Wallbox, WE24.P_pv_v, round(WE24.P_Netz_v,2)]

        connectSQ = sqlite3.connect(path2)
        cursorSQ = connectSQ.cursor()

        WE_list = [csv_list_we1,csv_list_we2,csv_list_we3,csv_list_we4,csv_list_we5,csv_list_we6,csv_list_we7,csv_list_we8,csv_list_we9,csv_list_we10,
                   csv_list_we11,csv_list_we12,csv_list_we13,csv_list_we14,csv_list_we15,csv_list_we16,csv_list_we17,csv_list_we18,csv_list_we19,csv_list_we20,csv_list_we21,csv_list_we22,csv_list_we23,csv_list_we24]

        #Idee: Wohneinheiten einzeln rausnehmen können!
        for i in range(24):
            cursorSQ.execute(f"CREATE TABLE IF NOT EXISTS WE{i+1}_sim1 "
                             "(Timestamp text PRIMARY KEY ,E_Bat real, SoC real,P_BSS real,P_Last real, P_Wallbox real, P_pv real,P_Netz real)")
        for i in range(24):
            cursorSQ.execute(f"INSERT OR IGNORE INTO WE{i+1}_sim1 "
                             "(Timestamp ,E_Bat, SoC,P_BSS,P_Last, P_Wallbox, P_pv,P_Netz) VALUES (?,?,?,?,?,?,?,?)",(WE_list[i]))
        for i in range(24):
            connectSQ.commit()
            for row in cursorSQ.execute(f"SELECT * FROM WE{i+1}_sim1"):
                row

    def run(self):
        while True:
            time.sleep(0.9)
            Zeitreihe.CSV_Daten()
class Handelstabelle(Thread):
    def __init__(self):
        super().__init__()

    def read_Handelsstatus(self):
        conn = sqlite3.connect('marketDB.db')
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
        self.P_bat_v_max = 2700
        self.Selbstentladung_v = (BSS.Selbstentladung/24)
        self.dE_v = 0
        self.P_load_v = 0
        self.load_offset = load_offset
        self.P_Netz_v = 0
        self.SoC_v = 50
        self.P_Wallbox = 0
        self.P_pv_v = 0
        self.PV_Handelsstatus = 0
        self.P_Residual_phy = 0
        self.P_Residual_v = 0
        self.countWE = 0
        self.Melani_Participation = 1
        self.Melani_NTn_count = 0

    def set_SOP(self):

        if self.PV_Handelsstatus == '0':
            self.P_pv_v = 0
        elif self.PV_Handelsstatus == '2':
            self.P_pv_v = P_pv * 2
        elif self.PV_Handelsstatus == '3':
            self.P_pv_v = P_pv * 3
        elif self.PV_Handelsstatus == '4':
            self.P_pv_v = P_pv * 4
        elif self.PV_Handelsstatus == '5':
            self.P_pv_v = P_pv * 5
        elif self.PV_Handelsstatus == '6':
            self.P_pv_v = P_pv * 6
        elif self.PV_Handelsstatus == '7':
            self.P_pv_v = P_pv * 7
        elif self.PV_Handelsstatus == '8':
            self.P_pv_v = P_pv * 8
        else:
            self.P_pv_v = P_pv
            # == 1


    def calc_parameters(self):
        self.P_Residual_phy = P_load_sum - P_pv_sum
        #print(self.P_Residual_phy)
        self.P_load_v = (P_Last * self.load_offset)
        self.P_Residual_v = self.P_load_v - self.P_pv_v
        self.E_bat_v = self.E_bat_v - self.Selbstentladung_v
        self.dE_v = (-self.P_load_v + self.P_pv_v) * (1/3600) * BSS.efficiency
        self.SoC_v = round(((self.E_bat_v/self.E_bat_v_max)*100),1)

    def strategy_ueberschussladen(self):


        if self.E_bat_v <= self.E_bat_v_min:
            'Entladegrenze virtuell -> SoC = 5%'
            #Konfiguration:  PV-Leistung geht auch bei SoC = 5% erst in die Lastabdeckung, dann in BSS-Ladung
            if self.P_pv_v >= self.P_load_v:
                self.E_bat_v = self.E_bat_v + self.dE_v
                self.P_bat_v = round(self.P_load_v - self.P_pv_v,2)
                self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

            elif self.P_pv_v < self.P_load_v:
                self.P_bat_v = 0
                self.P_Netz_v = self.P_load_v - self.P_pv_v

        elif self.E_bat_v + self.dE_v >= self.E_bat_v_max:  #SoC=100%
            'Virtueller Speicher ist voll'
            #print('Energiekonto von',self.Wohneinheit, 'ist voll, setze Ladeleistung P_bat = 0')
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        else:
            'Normalbetrieb: PV-Überschussladen'
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_bat_v = round(self.P_load_v - self.P_pv_v,2)       # bei PV-Überschuss negativer Wert -> Speicher laden!
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v # PV-Überschuss und Ladeleistung BSS gleichen sich im Normalbetrieb aus


    def strategy_depth_discharge_protection(self):
        'Entladegrenze physikalisch -> SoC = 5%'
        #Aufrechterhaltung ab SoC = 4,8%
        if BSS.E_bat_device <= 3650:
            self.P_bat_v = -25 - self.P_pv_v # Alle WE laden mit 25 W um SoC = 4,8% aufrecht zu erhalten
            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.P_Netz_v = self.P_load_v - self.P_bat_v
            self.E_bat_v = self.E_bat_v + self.dE_v

        elif P_pv_sum >= P_load_sum:
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_bat_v = round(self.P_load_v - self.P_pv_v,2)
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        elif P_pv_sum < P_load_sum:
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - self.P_pv_v


    def strategy_P_BSS_discharge_limit(self):
        if self.E_bat_v <= self.E_bat_v_min:
            'Entladegrenze virtuell -> SoC = 5%'
            #LISTE = []
            #Konfiguration:  PV-Leistung geht auch bei SoC = 5% erst in die Lastabdeckung, dann in BSS-Ladung
            if self.P_pv_v >= self.P_load_v:
                self.countWE = 0
                self.E_bat_v = self.E_bat_v + self.dE_v
                self.P_bat_v = round(self.P_load_v - self.P_pv_v,2)
                self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

            elif self.P_pv_v < self.P_load_v:
                self.countWE = 0
                self.P_bat_v = 0
                self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

        elif self.E_bat_v + self.dE_v >= self.E_bat_v_max:  #SoC=100%
            'Virtueller Speicher ist voll'
            self.countWE = 0
            self.P_bat_v = 0
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v
            self.P_Residual_v = 0  # Eigentlich negative Residuallast, aber wird 0 gesetzt für Berechnung von P_BSS_Mehrbedarf


            'Ab hier beginnt erst Entladeleistustungsbegrenzung'
        else:
            if (self.P_load_v - self.P_pv_v) < self.P_bat_v_max:
                'Normalbetrieb für WE unter der virtuellen Leistungsgrenze'
                self.countWE = 0
                self.P_bat_v = self.P_load_v - self.P_pv_v

            #elif (self.P_load_v - self.P_pv_v) >= self.P_bat_v_max and self.E_bat_v <= self.E_bat_v_min:


            elif (self.P_load_v - self.P_pv_v) >= self.P_bat_v_max:
                'Leistungsüberschreitende WE werden gedrosselt'
                P_BSS_Mehrbedarf = (self.P_Residual_phy - sum(P_res_v_emptyWE_sum)) - BSS.P_BSS_discharge_max # Ermittelt nötigen Netzbezug
                self.countWE = 1
                countWE_sum = sum(WE.countWE for WE in Wohneinheiten)
                P_AbzugsleistungProWE = (P_BSS_Mehrbedarf / countWE_sum) * 1.5  # 1.15 als Sicherheitsfaktor

                if ((self.P_load_v - self.P_pv_v) - P_AbzugsleistungProWE) <= self.P_bat_v_max: # Soll nicht unter 2,7 kW Grenze gedrosselt werden
                    self.P_bat_v = round(self.P_bat_v_max,1)
                else:
                    self.P_bat_v = round((self.P_load_v - self.P_pv_v) - P_AbzugsleistungProWE,1)

            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_Netz_v = self.P_load_v - self.P_pv_v - self.P_bat_v

    def run(self):  # AUFRUF DER BETRIEBSSTRATEGIE
        global LISTE
        global P_res_v_emptyWE_sum
        while True:
            try:
                P_res_v_emptyWE_sum = []
                P_res_v_emptyWE_sum = [W.P_Residual_v for W in Wohneinheiten if W.P_bat_v == 0]
                #print(P_res_v_emptyWE_sum,'SUMME -> ',sum(P_res_v_emptyWE_sum))

                for WE in Wohneinheiten:
                    WE.set_SOP()            # Setzt aktuellen SOP / Multiplikationsfaktor
                    WE.calc_parameters()    # Bestimme virtuellen Speicherstand etc.

                    if BSS.E_bat_device <= BSS.E_bat_min:
                        #print('Strategie: Tiefenentladungsschutz')
                        WE.strategy_depth_discharge_protection()
                        continue
                    elif (P_load_sum - P_pv_sum) - sum(P_res_v_emptyWE_sum) >= BSS.P_BSS_discharge_max:
                        #print('Strategie: Einladeleistungsbeschränkung')
                        WE.strategy_P_BSS_discharge_limit()
                    else:
                        #print('Strategie: PV-Überschussladen')
                        WE.strategy_ueberschussladen()



                self.P_BSS_sum = round(sum(WE.P_bat_v for WE in Wohneinheiten),1)
                self.E_bat_sum = round(sum(WE.E_bat_v for WE in Wohneinheiten),1)

                print('Simulierter Zeitstempel -->',Timestamp_sim,'--> P_pv =',P_pv_sum,'W')

            except NameError as err:
                print('NameError --->',str(err))

            time.sleep(1)



BSS = BSS_dummy()
PV = PV_dummy()
Last = Last_dummy()
Momentanwerte = MomentanwertDB()
Zeitreihe = ZeitreihenDB()
Handel = Handelstabelle()

WE1 = BSS_virtuell('WE1',0.35)  #WE,load_offset
WE2 = BSS_virtuell('WE2',0.8)
WE3 = BSS_virtuell('WE3',0.45)
WE4 = BSS_virtuell('WE4',0.3)
WE5 = BSS_virtuell('WE5',0.65)
WE6 = BSS_virtuell('WE6',0.55)
WE7 = BSS_virtuell('WE7',0.47)
WE8 = BSS_virtuell('WE8',0.33)
WE9 = BSS_virtuell('WE9',0.75)
WE10 = BSS_virtuell('WE10',0.39)
WE11 = BSS_virtuell('WE11',0.66)
WE12 = BSS_virtuell('WE12',0.31)
WE13 = BSS_virtuell('WE13',0.85)
WE14 = BSS_virtuell('WE14',0.69)
WE15 = BSS_virtuell('WE15',1.0)
WE16 = BSS_virtuell('WE16',0.25)
WE17 = BSS_virtuell('WE17',0.33)
WE18 = BSS_virtuell('WE18',0.8)
WE19 = BSS_virtuell('WE19',0.35)
WE20 = BSS_virtuell('WE20',0.45)
WE21 = BSS_virtuell('WE21',0.36)
WE22 = BSS_virtuell('WE22',0.75)
WE23 = BSS_virtuell('WE23',0.37)
WE24 = BSS_virtuell('WE24',0.39)
Wohneinheiten = [WE1, WE2, WE3, WE4, WE5, WE6, WE7, WE8, WE9, WE10, WE11, WE12,
                 WE13, WE14, WE15, WE16, WE17, WE18, WE19, WE20, WE21, WE22, WE23,WE24]


concurrentthreads = [PV,Last,BSS,Momentanwerte,WE1,Handel,Zeitreihe]
for threads in concurrentthreads:
    threads.start()
