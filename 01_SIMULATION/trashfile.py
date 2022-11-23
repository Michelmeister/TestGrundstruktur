import time
import datetime
timestamp = datetime.datetime.now()
Timestamp = str(timestamp.strftime("%m-%Y"))

def test():
    while True:
        #data.Momentanwertdatenbank()
        month = Timestamp
        if month == '11-2022':
            print('Es ist November')
            path2 = 'CSV_Datenbank\data_Nov22_sim1.db'
            open('data_' + month +'_sim1.txt','w')
            #data.CSV_Daten()
        elif month == '12-2022':
            print('Es ist Dezember')
            path2 = 'CSV_Datenbank\data_Dez22_sim1.db'
            #data.CSV_Daten()
        else:
            print('DAT LÄUFT NICHT')
        time.sleep(1)

test()
print(timestamp)
print(Timestamp)