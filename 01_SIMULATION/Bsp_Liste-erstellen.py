import time

class Wohneinheiten():
    def __init__(self,P):
        self.P = P

    def test(self):
        if self.P > 20:
            Leistungsliste.append(self.P)
            print(Leistungsliste)

        else:
            pass
        time.sleep(0.2)


WE1 = Wohneinheiten(10)
WE2 = Wohneinheiten(20)
WE3 = Wohneinheiten(30)
WE4 = Wohneinheiten(40)

Liste_WE = [WE1,WE2,WE3,WE4]

Leistungsliste = []

while True:

    #Leistungsliste = [WE.P for WE in Liste_WE if WE.P > 20]
    Leistungsliste = []
    for WE in Liste_WE:
        if WE.P > 20:
            Leistungsliste.append(WE.P)


    print(sum(Leistungsliste))
    time.sleep(1)