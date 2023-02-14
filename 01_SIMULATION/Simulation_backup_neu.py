from threading import Thread
import time
import csv
from datetime import datetime,timezone
import pytz
import sqlite3
import os

#########
P_load_sum      = 0
P_pv_sum        = 0
P_Wallbox_sum   = 0
NTn_count_sum   = 0
#########
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
                P_pv = round((48/7) * P_tot) # W, Skalierung von 7 auf 48 kWp
                #print(P_pv)
            Timestamp_sim = (row['Timestamp'])
            time.sleep(1)
class Last_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        p_last_we1 = p_last_we2 = p_last_we3 = p_last_we4 = p_last_we5 = p_last_we6 = p_last_we7 = p_last_we8 = 0
        p_last_we9 = p_last_we10 = p_last_we11 = p_last_we12 = p_last_we13 = p_last_we14 = p_last_we15 = p_last_we16 = 0
        p_last_we17 = p_last_we18 = p_last_we19 = p_last_we20 = p_last_we21 = p_last_we22 = p_last_we23 = p_last_we24 = 0

        p_last_list = [p_last_we1, p_last_we2, p_last_we3, p_last_we4, p_last_we5, p_last_we6, p_last_we7,
                       p_last_we8, p_last_we9, p_last_we10, p_last_we11, p_last_we12, p_last_we13,
                       p_last_we14, p_last_we15, p_last_we16, p_last_we17, p_last_we18, p_last_we19,
                       p_last_we20, p_last_we21, p_last_we22, p_last_we23, p_last_we24]

        csv_file_we1 = open('Last_csv\LP17_2010-06-23_06.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile_we1 = csv.DictReader(csv_file_we1,delimiter=',')
        csv_file_we2 = open('Last_csv\LP17_2010-06-23_04.56.00_to_2010-06-24_21.43.00_Mi.csv',newline='')
        load_profile_we2 = csv.DictReader(csv_file_we2,delimiter=',')
        csv_file_we3 = open('Last_csv\LP17_2010-06-27_06.00.00_to_2010-06-27_23.59.59_So.csv',newline='')
        load_profile_we3 = csv.DictReader(csv_file_we3,delimiter=',')
        csv_file_we4 = open('Last_csv\LP17_2010-06-23_18.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile_we4 = csv.DictReader(csv_file_we4,delimiter=',')
        csv_file_we5 = open('Last_csv\LP17_2010-06-26_00.00.00_to_2010-06-26_23.59.59_Sa.csv',newline='')
        load_profile_we5 = csv.DictReader(csv_file_we5,delimiter=',')
        csv_file_we6 = open('Last_csv\LP17_2010-06-23_12.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile_we6 = csv.DictReader(csv_file_we6,delimiter=',')
        csv_file_we7 = open('Last_csv\LP17_2010-06-27_00.00.00_to_2010-06-27_23.59.59_So.csv',newline='')
        load_profile_we7 = csv.DictReader(csv_file_we7,delimiter=',')
        csv_file_we8 = open('Last_csv\LP17_2010-12-22_12.00.00_to_2010-12-22_18.00.00_Mi.csv',newline='')
        load_profile_we8 = csv.DictReader(csv_file_we8,delimiter=',')
        csv_file_we9 = open('Last_csv\LP17_2010-12-26_00.00.00_to_2010-12-26_23.59.59_So.csv',newline='')
        load_profile_we9 = csv.DictReader(csv_file_we9,delimiter=',')
        csv_file_we10 = open('Last_csv\LP31_2010-06-27_18.00.00_to_2010-06-27_23.59.59_So.csv',newline='')
        load_profile_we10 = csv.DictReader(csv_file_we10,delimiter=',')
        csv_file_we11 = open('Last_csv\LP31_2010-12-26_12.00.00_to_2010-12-26_23.59.59_So.csv',newline='')
        load_profile_we11 = csv.DictReader(csv_file_we11,delimiter=',')
        csv_file_we12 = open('Last_csv\LP31_2010-06-23_00.00.00_to_2010-06-23_12.00.00_Mi.csv',newline='')
        load_profile_we12 = csv.DictReader(csv_file_we12,delimiter=',')
        csv_file_we13 = open('Last_csv\LP31_2010-12-26_06.00.00_to_2010-12-26_23.59.59_So.csv',newline='')
        load_profile_we13 = csv.DictReader(csv_file_we13,delimiter=',')
        csv_file_we14 = open('Last_csv\LP31_2010-12-22_06.00.00_to_2010-12-22_23.59.59_Mi.csv',newline='')
        load_profile_we14 = csv.DictReader(csv_file_we14,delimiter=',')
        csv_file_we15 = open('Last_csv\LP31_2010-12-25_18.00.00_to_2010-12-25_23.59.59_Sa.csv',newline='')
        load_profile_we15 = csv.DictReader(csv_file_we15,delimiter=',')
        csv_file_we16 = open('Last_csv\LP31_2010-06-23_21.43.00_to_2010-06-24_04.56.00_Mi.csv',newline='')
        load_profile_we16 = csv.DictReader(csv_file_we16,delimiter=',')
        csv_file_we17 = open('Last_csv\LP31_2010-12-25_06.00.00_to_2010-12-25_23.59.59_Sa.csv',newline='')
        load_profile_we17 = csv.DictReader(csv_file_we17,delimiter=',')
        csv_file_we18 = open('Last_csv\LP31_2010-12-26_06.00.00_to_2010-12-26_23.59.59_So.csv',newline='')
        load_profile_we18 = csv.DictReader(csv_file_we18,delimiter=',')
        csv_file_we19 = open('Last_csv\LP31_2010-12-18_00.00.00_to_2010-12-18_23.59.59_Sa.csv',newline='')
        load_profile_we19 = csv.DictReader(csv_file_we19,delimiter=',')
        csv_file_we20 = open('Last_csv\LP17_2010-12-22_16.07.00_to_2010-12-23_08.25.00_Mi.csv',newline='')
        load_profile_we20 = csv.DictReader(csv_file_we20,delimiter=',')
        csv_file_we21 = open('Last_csv\LP17_2010-06-23_04.56.00_to_2010-06-24_21.43.00_Mi.csv',newline='')
        load_profile_we21 = csv.DictReader(csv_file_we21,delimiter=',')
        csv_file_we22 = open('Last_csv\LP17_2010-12-15_18.00.00_to_2010-12-15_23.59.59_Mi.csv',newline='')
        load_profile_we22 = csv.DictReader(csv_file_we22,delimiter=',')
        csv_file_we23 = open('Last_csv\LP31_2010-12-18_00.00.00_to_2010-12-18_23.59.59_Sa.csv',newline='')
        load_profile_we23 = csv.DictReader(csv_file_we23,delimiter=',')
        csv_file_we24 = open('Last_csv\LP17_2010-06-23_06.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile_we24 = csv.DictReader(csv_file_we24,delimiter=',')

        load_profile_list = [load_profile_we1 ,load_profile_we2 , load_profile_we3, load_profile_we4, load_profile_we5, load_profile_we6, load_profile_we7, load_profile_we8, load_profile_we9, load_profile_we10, load_profile_we11, load_profile_we12, load_profile_we13, load_profile_we14, load_profile_we15, load_profile_we16, load_profile_we17, load_profile_we18, load_profile_we19, load_profile_we20, load_profile_we21, load_profile_we22, load_profile_we23, load_profile_we24]
        # & an Last-Variable der jeweiligen Wohneinheit übergeben
        for row in zip(*load_profile_list):
            for i in range(24):
                P1 = float(row[i]['P1'])
                #print(f"P1 aus Lastprofilnr. {i+1} = {P1}")
                P2 = float(row[i]['P2'])
                #print(f"P2 aus Lastprofilnr. {i+1} = {P2}")
                P3 = float(row[i]['P3'])
                #print(f"P3 aus Lastprofilnr. {i+1} = {P3}")
                p_last_list[i] = P1+P2+P3
                #print(f"Gesamtlast der WE{i+1} = {p_last_list[i]}")

            WE1.P_load_v = p_last_list[0] * 1.0
            WE2.P_load_v = p_last_list[1] * 0.85
            WE3.P_load_v = p_last_list[2] * 0.65
            WE4.P_load_v = p_last_list[3] * 0.75
            WE5.P_load_v = p_last_list[4] * 0.85
            WE6.P_load_v = p_last_list[5] * 0.45
            WE7.P_load_v = p_last_list[6] * 0.55
            WE8.P_load_v = p_last_list[7] * 0.65
            WE9.P_load_v = p_last_list[8] * 0.75
            WE10.P_load_v = p_last_list[9] * 0.55
            WE11.P_load_v = p_last_list[10] * 0.65
            WE12.P_load_v = p_last_list[11] * 0.45
            WE13.P_load_v = p_last_list[12] * 0.55
            WE14.P_load_v = p_last_list[13] * 0.65
            WE15.P_load_v = p_last_list[14] * 0.75
            WE16.P_load_v = p_last_list[15] * 0.85
            WE17.P_load_v = p_last_list[16] * 0.65
            WE18.P_load_v = p_last_list[17] * 0.45
            WE19.P_load_v = p_last_list[18] * 0.75
            WE20.P_load_v = p_last_list[19] * 0.55
            WE21.P_load_v = p_last_list[20] * 0.65
            WE22.P_load_v = p_last_list[21] * 0.75
            WE23.P_load_v = p_last_list[22] * 0.45
            WE24.P_load_v = p_last_list[23] * 0.55

            time.sleep(1)
class EV_charging_dummy(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        P_EV1 = P_EV2 = P_EV3 = P_EV4 = P_EV5 = P_EV6 = P_EV7 = P_EV8 = P_EV9 = P_EV10 = 0
        P_EV_list = [P_EV1, P_EV2, P_EV3, P_EV4, P_EV5, P_EV6, P_EV7, P_EV8, P_EV9, P_EV10]

        csv_EVfile1 = open('EV_csv/2020-01-06_Monday_manipuliert.csv', newline='')
        EV_profile1 = csv.DictReader(csv_EVfile1, delimiter=',')
        csv_EVfile2 = open('EV_csv/2020-01-07_Tuesday_manipuliert.csv', newline='')
        EV_profile2 = csv.DictReader(csv_EVfile2, delimiter=',')
        csv_EVfile3 = open('EV_csv/2020-01-08_Wednesday_manipuliert.csv', newline='')
        EV_profile3 = csv.DictReader(csv_EVfile3, delimiter=',')
        csv_EVfile4 = open('EV_csv/2020-01-09_Thursday_manipuliert.csv', newline='')
        EV_profile4 = csv.DictReader(csv_EVfile4, delimiter=',')
        csv_EVfile5 = open('EV_csv/2020-01-10_Friday_manipuliert.csv', newline='')
        EV_profile5 = csv.DictReader(csv_EVfile5, delimiter=',')
        csv_EVfile6 = open('EV_csv/2020-01-11_Saturday_manipuliert.csv', newline='')
        EV_profile6 = csv.DictReader(csv_EVfile6, delimiter=',')
        csv_EVfile7 = open('EV_csv/2020-01-06_Monday_manipuliert.csv', newline='')
        EV_profile7 = csv.DictReader(csv_EVfile7, delimiter=',')
        csv_EVfile8 = open('EV_csv/2020-01-07_Tuesday_manipuliert.csv', newline='')
        EV_profile8 = csv.DictReader(csv_EVfile8, delimiter=',')
        csv_EVfile9 = open('EV_csv/2020-01-08_Wednesday_manipuliert.csv', newline='')
        EV_profile9 = csv.DictReader(csv_EVfile9, delimiter=',')
        csv_EVfile10 = open('EV_csv/2020-01-06_Monday_manipuliert.csv', newline='')
        EV_profile10 = csv.DictReader(csv_EVfile10, delimiter=',')

        EV_profile_list = [EV_profile1, EV_profile2, EV_profile3, EV_profile4, EV_profile5,
                           EV_profile6, EV_profile7, EV_profile8, EV_profile9, EV_profile10]
        for row in zip(*EV_profile_list):
            for i in range(10):
                P_EV_list[i] = float(row[i]['Load_kW'])
                #print(P_EV_list[i], 'kW')
            WE2.P_Wallbox = round(P_EV_list[0] * 3) * 1000      # [*3 Phasen], [*1000 von kW auf W]
            WE5.P_Wallbox = round(P_EV_list[1] * 3) * 1000
            WE9.P_Wallbox = round(P_EV_list[2] * 3) * 1000
            WE13.P_Wallbox = round(P_EV_list[3] * 3) * 1000
            WE17.P_Wallbox = round(P_EV_list[4] * 3) * 1000
            WE18.P_Wallbox = round(P_EV_list[5] * 3) * 1000
            # WE19.P_Wallbox = round(P_EV_list[6] * 3) * 1000
            # WE20.P_Wallbox = round(P_EV_list[7] * 3) * 1000
            # WE21.P_Wallbox = round(P_EV_list[8] * 3) * 1000
            # WE22.P_Wallbox = round(P_EV_list[9] * 3) * 1000
            time.sleep(900)

class BSS_dummy(Thread):
    def __init__(self):
        super().__init__()
        self.E_bat_device = 30000 # Wh
        self.P_BSS_device = 0 # W # Sollwert für physikalische Lade-/Entladeleistung
        self.delta_E = 0

        self.E_bat_max = 67000 # Wh
        self.E_bat_min = 3350 # Untere Entladegrenze SoC = 5%
        self.SoC = 50
        self.efficiency = 0.85
        self.P_BSS_discharge_max = 65000 # W
        self.P_BSS_charge_max = -65000 #W
        self.Selbstentladung = ((0.03 * 67000)/24)/3600

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

class PV_excess_segment(Thread):
    def __init__(self):
        super().__init__()
        self.P_pv_excess_total = 0
        self.P_grid_excess_segment = 0

    def calc_pv_excess(self):
        P_pv_feedin_sum = round(sum(WE.P_pv_feedin for WE in Wohneinheiten),1)
        # print('P_pv_feedin_sum =',P_pv_feedin_sum)
        self.P_pv_excess_total = (P_pv * (NTn_count_sum/24)) + P_pv_feedin_sum
        # print('P_pv_excess_total =',self.P_pv_excess_total,'W')

    def calc_P_grid(self):
        P_grid2home = round(sum(WE.P_Netz_v for WE in Wohneinheiten),1)

        if self.P_pv_excess_total == 0:
            self.P_grid_excess_segment = 0

        elif self.P_pv_excess_total <= P_grid2home:
            self.P_grid_excess_segment = self.P_pv_excess_total

        elif self.P_pv_excess_total > P_grid2home:
            self.P_grid_excess_segment = P_grid2home - self.P_pv_excess_total

    def run(self):
        while True:
            PV_excess.calc_pv_excess()
            PV_excess.calc_P_grid()
            time.sleep(1)

        # ANMKERUNG: Überschuss evtl. in methode BSS_virtuell aufrufen, um Verzögerungen zu mindern!!!
        # Hier wäre dann nur die Strategie einzustellen

class MomentanwertDB(Thread):
    def __init__(self):
        super().__init__()

    def Momentanwertdatenbank(self):
        global P_load_sum
        global P_pv_sum
        global P_Wallbox_sum
        global Timestamp
        path = 'MomentanwertDB.db'
        timestamp = datetime.now(timezone.utc)
        local_time= timestamp.astimezone(pytz.timezone('Europe/Berlin'))
        Timestamp = str(local_time.strftime("%d-%m-%Y %H:%M:%S UTC%z"))
        # Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
        P_load_sum = round(sum(WE.P_load_v for WE in Wohneinheiten),1)
        P_pv_sum = round(sum(WE.P_pv_v for WE in Wohneinheiten),1)
        P_Wallbox_sum = round(sum(WE.P_Wallbox for WE in Wohneinheiten))
        P_grid_real = round(sum(WE.P_Netz_v for WE in Wohneinheiten),1)     # P_grid_real - Tatsächlicher Netzbezug (abzüglich PV-Überschussscheibe)
        P_grid_sum = P_grid_real                                            # P_grid_sum - Theoretisch notwendiger NetzBEZUG!

        if PV_excess.P_pv_excess_total >= P_grid_real:
            P_grid_real = 0
        elif PV_excess.P_pv_excess_total < P_grid_real:
            P_grid_real = P_grid_real - PV_excess.P_grid_excess_segment

        value_list = [
                    (Timestamp,'Geraetewerte',round(BSS.E_bat_device,2),BSS.SoC,BSS.P_BSS_device,P_load_sum, P_Wallbox_sum,P_pv_sum, round(P_grid_real,2)),
                    (Timestamp,'Rechenwerte', round(WE1.E_bat_sum,2), BSS.SoC, WE1.P_BSS_sum, P_load_sum, P_Wallbox_sum, P_pv_sum, round(P_grid_sum,2)),
                    (Timestamp,WE1.Wohneinheit, round(WE1.E_bat_v,2), WE1.SoC_v, WE1.P_bat_v, WE1.P_load_v, WE1.P_Wallbox, WE1.P_pv_usage, round(WE1.P_Netz_v,2)),
                    (Timestamp,WE2.Wohneinheit, round(WE2.E_bat_v,2), WE2.SoC_v, WE2.P_bat_v, WE2.P_load_v, WE2.P_Wallbox, WE2.P_pv_usage, round(WE2.P_Netz_v,2)),
                    (Timestamp,WE3.Wohneinheit, round(WE3.E_bat_v,2), WE3.SoC_v, WE3.P_bat_v, WE3.P_load_v, WE3.P_Wallbox, WE3.P_pv_usage, round(WE3.P_Netz_v,2)),
                    (Timestamp,WE4.Wohneinheit, round(WE4.E_bat_v,2), WE4.SoC_v, WE4.P_bat_v, WE4.P_load_v, WE4.P_Wallbox, WE4.P_pv_usage, round(WE4.P_Netz_v,2)),
                    (Timestamp,WE5.Wohneinheit, round(WE5.E_bat_v,2), WE5.SoC_v, WE5.P_bat_v, WE5.P_load_v, WE5.P_Wallbox, WE5.P_pv_usage, round(WE5.P_Netz_v,2)),
                    (Timestamp,WE6.Wohneinheit, round(WE6.E_bat_v,2), WE6.SoC_v, WE6.P_bat_v, WE6.P_load_v, WE6.P_Wallbox, WE6.P_pv_usage, round(WE6.P_Netz_v,2)),
                    (Timestamp,WE7.Wohneinheit, round(WE7.E_bat_v,2), WE7.SoC_v, WE7.P_bat_v, WE7.P_load_v, WE7.P_Wallbox, WE7.P_pv_usage, round(WE7.P_Netz_v,2)),
                    (Timestamp,WE8.Wohneinheit, round(WE8.E_bat_v,2), WE8.SoC_v, WE8.P_bat_v, WE8.P_load_v, WE8.P_Wallbox, WE8.P_pv_usage, round(WE8.P_Netz_v,2)),
                    (Timestamp,WE9.Wohneinheit, round(WE9.E_bat_v,2), WE9.SoC_v, WE9.P_bat_v, WE9.P_load_v, WE9.P_Wallbox, WE9.P_pv_usage, round(WE9.P_Netz_v,2)),
                    (Timestamp,WE10.Wohneinheit,round(WE10.E_bat_v,2),WE10.SoC_v,WE10.P_bat_v,WE10.P_load_v,WE10.P_Wallbox,WE10.P_pv_usage, round(WE10.P_Netz_v,2)),
                    (Timestamp,WE11.Wohneinheit,round(WE11.E_bat_v,2),WE11.SoC_v,WE11.P_bat_v,WE11.P_load_v,WE11.P_Wallbox,WE11.P_pv_usage, round(WE11.P_Netz_v,2)),
                    (Timestamp,WE12.Wohneinheit,round(WE12.E_bat_v,2),WE12.SoC_v,WE12.P_bat_v,WE12.P_load_v,WE12.P_Wallbox,WE12.P_pv_usage, round(WE12.P_Netz_v,2)),
                    (Timestamp,WE13.Wohneinheit,round(WE13.E_bat_v,2),WE13.SoC_v,WE13.P_bat_v,WE13.P_load_v,WE13.P_Wallbox,WE13.P_pv_usage, round(WE13.P_Netz_v,2)),
                    (Timestamp,WE14.Wohneinheit,round(WE14.E_bat_v,2),WE14.SoC_v,WE14.P_bat_v,WE14.P_load_v,WE14.P_Wallbox,WE14.P_pv_usage, round(WE14.P_Netz_v,2)),
                    (Timestamp,WE15.Wohneinheit,round(WE15.E_bat_v,2),WE15.SoC_v,WE15.P_bat_v,WE15.P_load_v,WE15.P_Wallbox,WE15.P_pv_usage, round(WE15.P_Netz_v,2)),
                    (Timestamp,WE16.Wohneinheit,round(WE16.E_bat_v,2),WE16.SoC_v,WE16.P_bat_v,WE16.P_load_v,WE16.P_Wallbox,WE16.P_pv_usage, round(WE16.P_Netz_v,2)),
                    (Timestamp,WE17.Wohneinheit,round(WE17.E_bat_v,2),WE17.SoC_v,WE17.P_bat_v,WE17.P_load_v,WE17.P_Wallbox,WE17.P_pv_usage, round(WE17.P_Netz_v,2)),
                    (Timestamp,WE18.Wohneinheit,round(WE18.E_bat_v,2),WE18.SoC_v,WE18.P_bat_v,WE18.P_load_v,WE18.P_Wallbox,WE18.P_pv_usage, round(WE18.P_Netz_v,2)),
                    (Timestamp,WE19.Wohneinheit,round(WE19.E_bat_v,2),WE19.SoC_v,WE19.P_bat_v,WE19.P_load_v,WE19.P_Wallbox,WE19.P_pv_usage, round(WE19.P_Netz_v,2)),
                    (Timestamp,WE20.Wohneinheit,round(WE20.E_bat_v,2),WE20.SoC_v,WE20.P_bat_v,WE20.P_load_v,WE20.P_Wallbox,WE20.P_pv_usage, round(WE20.P_Netz_v,2)),
                    (Timestamp,WE21.Wohneinheit,round(WE21.E_bat_v,2),WE21.SoC_v,WE21.P_bat_v,WE21.P_load_v,WE21.P_Wallbox,WE21.P_pv_usage, round(WE21.P_Netz_v,2)),
                    (Timestamp,WE22.Wohneinheit,round(WE22.E_bat_v,2),WE22.SoC_v,WE22.P_bat_v,WE22.P_load_v,WE22.P_Wallbox,WE22.P_pv_usage, round(WE22.P_Netz_v,2)),
                    (Timestamp,WE23.Wohneinheit,round(WE23.E_bat_v,2),WE23.SoC_v,WE23.P_bat_v,WE23.P_load_v,WE23.P_Wallbox,WE23.P_pv_usage, round(WE23.P_Netz_v,2)),
                    (Timestamp,WE24.Wohneinheit,round(WE24.E_bat_v,2),WE24.SoC_v,WE24.P_bat_v,WE24.P_load_v,WE24.P_Wallbox,WE24.P_pv_usage, round(WE24.P_Netz_v,2)),
                    (Timestamp,'Zusatzsegment',0,0,0,0,0,round(PV_excess.P_pv_excess_total,2), round(PV_excess.P_grid_excess_segment, 2))
                      ]
        conSQ = sqlite3.connect(path)
        curSQ = conSQ.cursor()
        curSQ.execute("CREATE TABLE IF NOT EXISTS Tabelle1 "
                      "(Timestamp text, Name text PRIMARY KEY,E_BSS real, SoC real,P_BSS real, P_Last real, P_Wallbox real,P_PV_Nutz real, P_Netz real)")
        curSQ.executemany("INSERT OR REPLACE INTO Tabelle1 "
                          "(Timestamp, Name, E_BSS, SoC,P_BSS, P_Last, P_Wallbox,P_PV_Nutz, P_Netz) VALUES (?,?,?,?,?,?,?,?,?)",(value_list))
        conSQ.commit()
        for row in curSQ.execute("SELECT * FROM Tabelle1"):
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

        # Zeitstempel wird erstellt
        time = datetime.now()
        timestamp = datetime.now(timezone.utc)
        local_time = timestamp.astimezone(pytz.timezone('Europe/Berlin'))
        Timestamp = str(local_time.strftime("%d-%m-%Y %H:%M:%S UTC%z"))

        # Ordner- & Dateiname festlegen
        csv_name = str(time.strftime("%d%b%Y"))
        directory = str(time.strftime("%Y_%m"))
        parent_dir = 'ZeitreihenDB'  # muss angepasst werden, je nach dem wo Ordner liegt!
        path = os.path.join(parent_dir, directory)

        # sucht nach Ordner des aktuellen Monats, falls nicht vorhanden, wird neuer Ordner erstellt
        try:
            os.stat(path)
            #print("Ordner '%s' bereits vorhanden" % directory)
        except:
            os.mkdir(path)
            #print("Ordner '%s' erstellt" % directory)

        path2 = path + '/data_' + csv_name + '.db'

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

        # SQlite-Datenbank wird erstellt
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
            time.sleep(0.49)
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
class Melani_Participation(Thread):
    def __init__(self):
        super().__init__()

    def read_Participation_status(self):
        global NTn_count_sum
        conn = sqlite3.connect('Teilnehmerliste.db')
        cc = conn.cursor()
        cc.execute('SELECT * FROM Teilnehmer')
        value = cc.fetchall()

        WE1.Participation_status = value[1][1]
        WE2.Participation_status = value[2][1]
        WE3.Participation_status = value[3][1]
        WE4.Participation_status = value[4][1]
        WE5.Participation_status = value[5][1]
        WE6.Participation_status = value[6][1]
        WE7.Participation_status = value[7][1]
        WE8.Participation_status = value[8][1]
        WE9.Participation_status = value[9][1]
        WE10.Participation_status = value[10][1]
        WE11.Participation_status = value[11][1]
        WE12.Participation_status = value[12][1]
        WE13.Participation_status = value[13][1]
        WE14.Participation_status = value[14][1]
        WE15.Participation_status = value[15][1]
        WE16.Participation_status = value[16][1]
        WE17.Participation_status = value[17][1]
        WE18.Participation_status = value[18][1]
        WE19.Participation_status = value[19][1]
        WE20.Participation_status = value[20][1]
        WE21.Participation_status = value[21][1]
        WE22.Participation_status = value[22][1]
        WE23.Participation_status = value[23][1]
        WE24.Participation_status = value[24][1]

        for WE in Wohneinheiten:
            if WE.Participation_status == 1:
                WE.Melani_NTn_count = 0
            else:
                WE.Melani_NTn_count = 1
                # Wenn Status 0 ist nimmt die WE nicht teil, der Counter erhöht sich um 1

        NTn_count_sum = sum(WE.Melani_NTn_count for WE in Wohneinheiten)
        #print('NTn-Count =',NTn_count_sum)

    def run(self):
        while True:
            Participation.read_Participation_status()
            #print(WE1.Wohneinheit,'Participation_Status = ',WE1.Participation_status)
            time.sleep(1)

class BSS_virtuell(Thread):
    def __init__(self,Wohneinheit):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.P_bat_v = 0
        self.E_bat_v = (BSS.E_bat_device/24)
        self.E_bat_v_max = (BSS.E_bat_max/24) # = 2791.67
        self.E_bat_v_min = 139.5
        self.E_bat_sum = 35000 # initial value
        self.P_BSS_sum = 0
        self.P_bat_v_max = 2700
        self.dE_v = 0
        self.P_load_v = 0
        self.P_Netz_v = 0
        self.SoC_v = 50
        self.P_Wallbox = 0
        self.P_pv_v = 0
        self.P_pv_usage = 0
        self.P_pv_feedin = 0
        self.PV_Handelsstatus = 0
        self.P_Residual_phy = 0
        self.P_Residual_v = 0
        self.countWE = 0
        self.Participation_status = 1
        self.Melani_NTn_count = 0
        self.Selbstentladung_v = (BSS.Selbstentladung/(24-NTn_count_sum))

    def set_SOP(self):

        if self.PV_Handelsstatus == '0':
            self.P_pv_v = 0
        elif self.PV_Handelsstatus == '2':
            self.P_pv_v = P_pv * (2/24)
        elif self.PV_Handelsstatus == '3':
            self.P_pv_v = P_pv * (3/24)
        elif self.PV_Handelsstatus == '4':
            self.P_pv_v = P_pv * (4/24)
        elif self.PV_Handelsstatus == '5':
            self.P_pv_v = P_pv * (5/24)
        elif self.PV_Handelsstatus == '6':
            self.P_pv_v = P_pv * (6/24)
        elif self.PV_Handelsstatus == '7':
            self.P_pv_v = P_pv * (7/24)
        elif self.PV_Handelsstatus == '8':
            self.P_pv_v = P_pv * (8/24)
        else:
            self.P_pv_v = P_pv * (1/24)
            # == 1

        self.P_pv_v = round(self.P_pv_v,2) # Macht nichts außer Wert zu runden -> Achtung, später nur für Anzeige in DB runden, Rechnungswerte werden verfälscht!

    def calc_parameters(self):
        self.P_Residual_phy = P_load_sum + P_Wallbox_sum - P_pv_sum
        self.P_Residual_v = self.P_load_v + self.P_Wallbox - self.P_pv_v
        self.E_bat_v = self.E_bat_v - self.Selbstentladung_v
        self.dE_v = (-self.P_load_v - self.P_Wallbox + self.P_pv_v) * (1/3600) * BSS.efficiency
        self.SoC_v = round(((self.E_bat_v/self.E_bat_v_max)*100),1)

    def strategy_ueberschussladen(self):
        if self.E_bat_v <= self.E_bat_v_min:
            'Entladegrenze virtuell -> SoC = 5%'
            #Konfiguration:  PV-Leistung geht auch bei SoC = 5% erst in die Lastabdeckung, dann in BSS-Ladung
            if self.P_pv_v >= self.P_load_v + self.P_Wallbox:
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0
                self.E_bat_v = self.E_bat_v + self.dE_v
                self.P_bat_v = round(self.P_load_v + self.P_Wallbox - self.P_pv_v,2)
                self.P_Netz_v = 0

            elif self.P_pv_v < self.P_load_v + self.P_Wallbox:
                self.P_bat_v = 0
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0
                self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v

        elif self.E_bat_v + self.dE_v >= self.E_bat_v_max:  #SoC=100%
            'Virtueller Speicher ist voll'
            self.P_pv_usage = self.P_load_v
            self.P_pv_feedin = self.P_pv_v - self.P_pv_usage
            self.P_bat_v = 0
            # self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v
            self.P_Netz_v = 0

        else:
            'Normalbetrieb: PV-Überschussladen'
            self.P_bat_v = round(self.P_load_v + self.P_Wallbox - self.P_pv_v,2)  # bei PV-Überschuss negativer Wert -> Speicher laden!
            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_pv_usage = self.P_pv_v
            self.P_pv_feedin = 0
            self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v # PV-Überschuss und Ladeleistung BSS gleichen sich im Normalbetrieb aus


    def strategy_depth_discharge_protection(self):
        'Entladegrenze physikalisch -> SoC = 5%'
        if BSS.E_bat_device <= (0.05 * BSS.E_bat_max):
            self.P_pv_usage = self.P_pv_v
            self.P_pv_feedin = 0
            if P_pv_sum >= P_load_sum + P_Wallbox_sum:
                if self.P_pv_v >= self.P_load_v + self.P_Wallbox:
                    self.E_bat_v = self.E_bat_v + self.dE_v
                    self.P_bat_v = round(self.P_load_v + self.P_Wallbox - self.P_pv_v,2)
                    self.P_Netz_v = 0

                elif self.P_pv_v < self.P_load_v + self.P_Wallbox:
                    self.P_bat_v = 0
                    self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v


            elif BSS.E_bat_device <= (0.045 * BSS.E_bat_max):
                'Erhaltungsladung von SoC = 4,5 bis 4,8%'
                self.P_bat_v = -25
                self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_bat_v - self.P_pv_v
                self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
                self.E_bat_v = self.E_bat_v + self.dE_v
            elif BSS.E_bat_device >= (0.048 * BSS.E_bat_max):
                self.P_bat_v = 0
                self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_bat_v - self.P_pv_v
            else:
                # Bleibe in Erhaltungsladung bis SoC = 4,8%
                self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_bat_v - self.P_pv_v
                self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
                self.E_bat_v = self.E_bat_v + self.dE_v


    def strategy_P_BSS_discharge_limit(self):
        if self.E_bat_v <= self.E_bat_v_min:
            'Entladegrenze virtuell -> SoC = 5%'
            #Konfiguration:  PV-Leistung geht auch bei SoC = 5% erst in die Lastabdeckung, dann in BSS-Ladung
            if self.P_pv_v >= self.P_load_v + self.P_Wallbox:
                self.countWE = 0
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0
                self.E_bat_v = self.E_bat_v + self.dE_v
                self.P_bat_v = round(self.P_load_v + self.P_Wallbox - self.P_pv_v,2)
                self.P_Netz_v = 0

            elif self.P_pv_v < self.P_load_v + self.P_Wallbox:
                self.countWE = 0
                self.P_bat_v = 0
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0
                self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v

        elif self.E_bat_v + self.dE_v >= self.E_bat_v_max:  #SoC=100%
            'Virtueller Speicher ist voll'
            self.countWE = 0
            self.P_bat_v = 0
            self.P_pv_usage = self.P_load_v
            self.P_pv_feedin = self.P_pv_v - self.P_pv_usage
            self.P_Netz_v = 0
            # self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v
            self.P_Residual_v = 0  # Eigentlich negative Residuallast, aber wird 0 gesetzt für Berechnung von P_BSS_Mehrbedarf


            'Ab hier beginnt erst Entladeleistustungsbegrenzung'
        else:
            if (self.P_load_v + self.P_Wallbox - self.P_pv_v) < self.P_bat_v_max:
                'Normalbetrieb für WE unter der virtuellen Leistungsgrenze'
                self.countWE = 0
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0
                self.P_bat_v = self.P_load_v + self.P_Wallbox - self.P_pv_v

            elif (self.P_load_v + self.P_Wallbox - self.P_pv_v) >= self.P_bat_v_max:
                'Leistungsüberschreitende WE werden gedrosselt'
                P_BSS_Mehrbedarf = (self.P_Residual_phy) - (sum(P_res_v_emptyWE_sum)) - BSS.P_BSS_discharge_max # Ermittelt nötigen Netzbezug,  + sum(P_EV_v_emptyWE_sum)
                self.countWE = 1
                countWE_sum = sum(WE.countWE for WE in Wohneinheiten)
                #print('count =',countWE_sum)
                P_AbzugsleistungProWE = (P_BSS_Mehrbedarf / countWE_sum) * 1.15  # 1.15 als Sicherheitsfaktor
                self.P_pv_usage = self.P_pv_v
                self.P_pv_feedin = 0

                if ((self.P_load_v + self.P_Wallbox - self.P_pv_v) - P_AbzugsleistungProWE) <= self.P_bat_v_max: # Soll nicht unter 2,7 kW Grenze gedrosselt werden
                    self.P_bat_v = round(self.P_bat_v_max,1)
                else:
                    self.P_bat_v = round((self.P_load_v + self.P_Wallbox - self.P_pv_v) - P_AbzugsleistungProWE,1)

            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v

    def set_NTn_parameters(self):
        #print(self.Wohneinheit, 'status = ', self.Participation_status)
        #self.E_bat_v = 0
        #self.E_bat_v = self.E_bat_v + self.Selbstentladung_v
        self.P_bat_v = 0
        self.SoC_v = 0 # round(((self.E_bat_v / self.E_bat_v_max) * 100), 1)
        self.P_pv_v = 0
        self.P_pv_usage = self.P_pv_v
        self.P_pv_feedin = 0
        self.P_Residual_v = self.P_load_v
        self.P_Netz_v = self.P_load_v + self.P_Wallbox


    def run(self):  # AUFRUF DER BETRIEBSSTRATEGIE
        'STRATEGIEAUFRUF !!!'
        global P_res_v_emptyWE_sum
        global P_EV_v_emptyWE_sum
        while True:
            try:
                P_res_v_emptyWE_sum = []
                P_res_v_emptyWE_sum = [W.P_Residual_v for W in Wohneinheiten if W.P_bat_v == 0]
                P_EV_v_emptyWE_sum = []
                P_EV_v_emptyWE_sum = [W.P_Wallbox for W in Wohneinheiten if W.P_bat_v == 0]
                #print('Summenliste =',sum(P_EV_v_emptyWE_sum))
                #print(P_res_v_emptyWE_sum,'SUMME -> ',sum(P_res_v_emptyWE_sum))

                for WE in Wohneinheiten:
                    if WE.Participation_status == 0:
                        WE.set_NTn_parameters()
                    else:
                        WE.set_SOP()            # Setzt aktuellen SOP / Multiplikationsfaktor
                        WE.calc_parameters()    # Bestimme virtuellen Speicherstand etc.

                        if BSS.E_bat_device <= BSS.E_bat_min:
                            #print('Strategie: Tiefenentladungsschutz')
                            WE.strategy_depth_discharge_protection()
                            continue
                        elif (P_load_sum + P_Wallbox_sum - P_pv_sum) - (sum(P_res_v_emptyWE_sum)) >= BSS.P_BSS_discharge_max: # + sum(P_EV_v_emptyWE_sum)
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

EV = EV_charging_dummy()
Participation = Melani_Participation()
PV_excess = PV_excess_segment()
BSS = BSS_dummy()
PV = PV_dummy()
Last = Last_dummy()
Momentanwerte = MomentanwertDB()
Zeitreihe = ZeitreihenDB()
Handel = Handelstabelle()


WE1 = BSS_virtuell('WE1')
WE2 = BSS_virtuell('WE2')
WE3 = BSS_virtuell('WE3')
WE4 = BSS_virtuell('WE4')
WE5 = BSS_virtuell('WE5')
WE6 = BSS_virtuell('WE6')
WE7 = BSS_virtuell('WE7')
WE8 = BSS_virtuell('WE8')
WE9 = BSS_virtuell('WE9')
WE10 = BSS_virtuell('WE10')
WE11 = BSS_virtuell('WE11')
WE12 = BSS_virtuell('WE12')
WE13 = BSS_virtuell('WE13')
WE14 = BSS_virtuell('WE14')
WE15 = BSS_virtuell('WE15')
WE16 = BSS_virtuell('WE16')
WE17 = BSS_virtuell('WE17')
WE18 = BSS_virtuell('WE18')
WE19 = BSS_virtuell('WE19')
WE20 = BSS_virtuell('WE20')
WE21 = BSS_virtuell('WE21')
WE22 = BSS_virtuell('WE22')
WE23 = BSS_virtuell('WE23')
WE24 = BSS_virtuell('WE24')
Wohneinheiten = [WE1, WE2, WE3, WE4, WE5, WE6, WE7, WE8, WE9, WE10, WE11, WE12,
                 WE13, WE14, WE15, WE16, WE17, WE18, WE19, WE20, WE21, WE22, WE23,WE24]

concurrentthreads = [Participation,PV,Last,EV,BSS,Momentanwerte,WE1,Handel,PV_excess] #Zeitreihe
for threads in concurrentthreads:
    threads.start()
