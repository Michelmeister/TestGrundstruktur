from threading import Thread
from random import randint
import time

class WRbat(Thread):
    def __init__(self,name,IPadr,port):
        super().__init__()
        self.name   = name
        self.IPadr  = '134.169.132.234'
        self.port   = '502'

    def get_SoC(self):
        return 47

    def get_Temp(self):
        return randint(24,27)

    def run(self):
            for n in range(0,10):
                print('SoC =',self.get_SoC(),'%')
                print('T_bat =',self.get_Temp(),'°C')
                time.sleep(0.5)