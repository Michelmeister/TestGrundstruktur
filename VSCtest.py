import time,sched
from datetime import datetime


def action():
    print('Zeitversetzte Funktion')
    time.sleep(1)
    print('Test 1')
    time.sleep(10)
    print('Test 2')

#while True:
 #   now = datetime.now()
  #  if now.hour == 13 and now.minute == 37 and now.second == 20:
   #     action()
    #    break

#print(now)

t = 0
min = 0
for row in range(0,180):
    t = t + 1
    if t == 60:
        t = 0
        min = min +1
    s = t
    #time.sleep(1)
    print('Timestamp',min,'min',s,'s')
    time.sleep(1)
