import csv
import time
from threading import Thread

global P_soll
class Lastprofil(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global P_soll
        csv_file = open('LP17_2010-06-23_00.00.00_to_2010-06-23_23.59.59_Mi.csv',newline='')
        load_profile = csv.DictReader(csv_file,delimiter=',')
        for row in load_profile:
            P1 = float(row['P1'])
            P_soll = P1 * 3
            print(row['Timestamp'],'--->',P_soll,'W')
            time.sleep(1)


if __name__ == '__main__':
    Lastabfrage = Lastprofil()
    Lastabfrage.run()
