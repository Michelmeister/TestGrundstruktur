from threading import Thread
from random import randint
import time

class WRpv(Thread):
    def __init__(self,name,IPadr,port):
        super().__init__()
        self.name   = name
        self.IPadr  = '134.169.132.235'
        self.port   = '502'

    def get_P(self):
        return randint(0,10)

    def run(self):
        for n in range(0,10):
            print('P_pv =',self.get_P(),'kW')
            time.sleep(0.5)

#PVinv = WRpv('PV','134.169.132.235','502')
#PVinv.run()
