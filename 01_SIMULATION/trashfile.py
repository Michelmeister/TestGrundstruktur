import time

for dE in range (0,3600):
    P = 1000 # W
    E_bat = (dE + (P * 1/3600))
    print('E_bat =',dE,'Wh')
    time.sleep(1)