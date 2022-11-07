import time
from threading import Thread
import devices.PVinverter.STP5040 as STP50
import devices.BATinverter.STPS60 as STPS60
import laboratory.DCquelle.DC as DC
import laboratory.Last.Socket_load_values as LM

PVinverter  = STP50.STP50(ipadr='134.169.132.235')
BATinverter = STPS60.STPS60(ipadr='134.169.132.230')
### LABORUMGEBUNG ###
DCsource    = DC.DCquelle(ipadr='134.169.132.167')
Receiver    = LM.Receiver()

class OperationManagement(Thread):
    def __init__(self):
        super().__init__()



    def run(self):
        while True:
            if Receiver.get_P_load() == None:
                P_load = 0
            else:
                P_load = Receiver.get_P_load()

            if PVinverter.get_P_ac() == None:
                P_pv_ac = 0
            else:
                P_pv_ac = PVinverter.get_P_ac()

            if BATinverter.get_SoC() == None:
                SoC = 0
            else:
                SoC = BATinverter.get_SoC()

            print('Hotfix test -> P_pv_ac =', P_pv_ac )
            print('Hotfix test -> SoC = ',SoC,'%')
            print('Hotfix test -> P_load =',P_load)

            if P_load > P_pv_ac and SoC > 7:
                Entladeleistung = P_load - P_pv_ac
                P_proz = (Entladeleistung/75000)*100*100            # 75 000 Wechselrichter-abhängig
                BATinverter.set_P(P_proz)

            elif P_pv_ac > P_load and SoC < 100:
                Ladeleistung = P_pv_ac - P_load
                P_prozent = (Ladeleistung/75000)*100*100            # WECHSELRICHTER-ABHÄNGIG
                BATinverter.set_P(-P_prozent)
                #print('Batterie soll geladen werden')
            elif P_load == P_pv_ac:
                BATinverter.set_P(00)
            time.sleep(0.3)



