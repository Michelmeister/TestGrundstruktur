from threading import Thread
import time
from datetime import datetime,timezone
import pytz
#from Simulation import *

class BSS():
    def __init__(self):
        self.E_bat = 0
        self.P_bat = P_bat
        self.E_bat_max = 3167

    def Energiefluss(self):
        while True:
            print('E_bat =',self.E_bat,'kWh & P_bat =',P_bat,'kW & E_bat_max =',self.E_bat_max,'kWh')
            self.E_bat = self.E_bat + 1 # kWh
            time.sleep(1)
#P_bat = 10 #kW
# #BSS_Aufruf = BSS()
#BSS_Aufruf.Energiefluss()


timestamp = datetime.now(timezone.utc)
local_time= timestamp.astimezone(pytz.timezone('Europe/Berlin'))
Timestamp = str(local_time.strftime("%d-%m-%Y %H:%M:%S UTC%z"))

print(Timestamp)

