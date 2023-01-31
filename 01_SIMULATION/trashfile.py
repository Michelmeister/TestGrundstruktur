from threading import Thread
import sqlite3
import time


class BSS_virtuell(Thread):
    def __init__(self,Wohneinheit):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.Teilnahmestatus = 1
        self.P = 0

    def run(self):
        while True:
            print(self.Wohneinheit,'P =',self.P)
            time.sleep(3.25)
class Nichtteilnehmer(Thread):
    def __init__(self,Wohneinheit):
        super().__init__()
        self.Wohneinheit = Wohneinheit
        self.Teilnahmestatus = 0
        self.P = 100

    def run(self):
        while True:
            print(self.Wohneinheit,'P =',self.P)
            time.sleep(3)

class Teilnahmeliste(Thread):
    def __init__(self):
        super().__init__()

    def read_Teilnahmestatus(self):
        conn = sqlite3.connect('Teilnehmerliste.db')
        cc = conn.cursor()
        cc.execute('SELECT * FROM Teilnehmer')
        value = cc.fetchall()

        TeilnahmestatusWE1 = value[1][1]
        #print(TeilnahmestatusWE1)

    def run(self):
        while True:
            Teilnahme.read_Teilnahmestatus()

            time.sleep(1)

Teilnahme = Teilnahmeliste()
WE1 = BSS_virtuell('WE1')
WE2 = BSS_virtuell('WE2')
WE3 = BSS_virtuell('WE3')
WE4 = BSS_virtuell('WE4')
WE1_ntn = Nichtteilnehmer('WE1_ntn')
WE2_ntn = Nichtteilnehmer('WE2_ntn')
WE3_ntn = Nichtteilnehmer('WE3_ntn')
WE4_ntn = Nichtteilnehmer('WE4_ntn')

Wohneinheiten_Melani = []
Wohneinheiten_NTn = []

Wohneinheiten_Melani = [W.P_Residual_v for W in Wohneinheiten if W.P_bat_v == 0]


concurrentthreads = [Teilnahme,WE1,WE1_ntn]
for threads in concurrentthreads:
    threads.start()

if self.Teilnahme == 0:
    self.P_bat_v = 0
    self.SoC = 0
    self.P_pv_v = 0
    ...
    self.P_Netz = self.load
    self.P_Res_v = self.load
else:
    ...
