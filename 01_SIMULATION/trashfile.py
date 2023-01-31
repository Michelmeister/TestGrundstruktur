import time
from threading import Thread
import csv
from datetime import datetime

class EV_charging_dummy(Thread):
    def __init__(self):
        super().__init__()
        self.P_charge = 0

    def run(self):
        global P_EV
        P_EV = 0
        csv_EVfile1 = open('EV_csv/2020-01-06_Monday_manipuliert.csv',newline='')
        csv_EVfile2 = open('EV_csv/2020-01-07_Tuesday_manipuliert.csv', newline='')
        csv_EVfile3 = open('EV_csv/2020-01-08_Wednesday_manipuliert.csv', newline='')
        csv_EVfile4 = open('EV_csv/2020-01-09_Thursday_manipuliert.csv', newline='')
        csv_EVfile5 = open('EV_csv/2020-01-10_Friday_manipuliert.csv', newline='')
        csv_EVfile6 = open('EV_csv/2020-01-11_Saturday_manipuliert.csv', newline='')

        EV_profile1 = csv.DictReader(csv_EVfile1, delimiter=',')
        EV_profile2 = csv.DictReader(csv_EVfile2, delimiter=',')
        EV_profile3 = csv.DictReader(csv_EVfile3, delimiter=',')
        EV_profile4 = csv.DictReader(csv_EVfile4, delimiter=',')
        EV_profile5 = csv.DictReader(csv_EVfile5, delimiter=',')
        EV_profile6 = csv.DictReader(csv_EVfile6, delimiter=',')

        for row in EV_profile1:
            P_EV = float(row['Load_kW'])
            P1 = round(P_EV * 3)
            print(P1,'kW')

            time.sleep(1)


Aufruf = EV_charging_dummy()

Aufruf.run()

