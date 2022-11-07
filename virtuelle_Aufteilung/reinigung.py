def write_Database(self):
    global P_pv
    global P_bat_real
    path = 'MomentanwertDB_test1.db'
    timestamp = datetime.datetime.now()
    Timestamp = str(timestamp.strftime("%d-%m-%Y %H:%M:%S"))
    value_list = [
        (Timestamp, 'Gerätewerte', E_bat_sum, SoC_sum, P_bat_real, P_load_sum, P_pv * 5, P_Netz_sum),
    ]
    conSQ = sqlite3.connect(path)
    curSQ = conSQ.cursor()
    curSQ.execute("CREATE TABLE IF NOT EXISTS aTest2 "
                  "(Timestamp text, x text PRIMARY KEY,E_bat real, SoC real,P_BSS real, P_Last real,P_PV real, P_Netz real)")
    curSQ.executemany("INSERT OR REPLACE INTO aTest2 "
                      "(Timestamp, x, E_bat, SoC,P_BSS, P_Last,P_PV, P_Netz) VALUES (?,?,?,?,?,?,?,?)", (value_list))
    conSQ.commit()
    for row in curSQ.execute("SELECT * FROM aTest2"):
        row