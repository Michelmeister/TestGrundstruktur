import time
import csv



m = open('Mittagszeit.csv',newline='')
Mittagsverlauf = csv.DictReader(m,delimiter=';')

f = open('PVokerufer.csv',newline='')
PVgen = csv.DictReader(f,delimiter=';')




def row_count():
    count = sum(1 for item in PVgen)
    print(count,'Zeilen')

def Mittagszeit():
    for row in Mittagsverlauf:
        if row['P_TOTAL'] == '' or row['Einstrahlung'] == '':
            print('Ungültiger Wert, halte vorherigen Wert')
            time.sleep(1)
        else:
            P_pv = float(row['P_TOTAL'])
            print(row['Timestamp'],'Einstrahlung G =',row['Einstrahlung'],'W/m² ?? -> P_pv =',round(P_pv),'W')
            time.sleep(1)

def full_day():
    for row in PVgen:
        if row['P_TOTAL'] == '':           # Später als if string empty -> hold value oder so!!!
            P_pv = 0.0
            print(row['Timestamp'],'-> P_pv =',P_pv,'W -> type:',type(P_pv))
        else:
            P_pv = float(row['P_TOTAL'])
            print(row['Timestamp'],'-> P_pv =',P_pv,'W -> type:',type(P_pv))
        time.sleep(1)

# das csv_lesen-Methode einfach mit in die set.Sollwerte-Methode, muss nicht aus Funktion extrahiert werden
# if == '' dann value hold -> einfach pass-Anweisung und trz ne Sekunde sleepmode!!!!!

# mitten in csv starten
# -> Möglichkeit, einfach csv irrelevante Teile rauslöschen


if __name__ == '__main__':
    try:
        #full_day()
        Mittagszeit()


        #row_count()
    except KeyboardInterrupt:
        print('\n',' -> Funktion wurde manuell unterbrochen!')


#while True:
 #   now = datetime.now()
  #  if now.hour == 13 and now.minute == 37 and now.second == 20:
   #     action()
    #    break

