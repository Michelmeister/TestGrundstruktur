### EMS EMS RECEIVER 05.09 ###

import socket
import time
import struct
from threading import Thread

class Receiver(Thread):
  def __init__(self):
    super().__init__()

  def get_P_load(self):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 10)
        s.settimeout(0.2)       # Timeout, damit andere Skripte weiterlaufen können
        s.connect(('134.169.132.217', 42424))
        msg = s.recv(1024)               # Will receive the reply message string from the server at 1024 B
        P_soll = float(msg.decode())
        time.sleep(0.2)

        s.shutdown(socket.SHUT_RDWR)
        s.close()

        return P_soll
    except socket.error as err:
      print('Socket Error in Socket_load_values.py',str(err))
      pass


  def run(self):
    self.get_P_load()



if __name__ == '__main__':
    Receiver = Receiver()

    print('P =',Receiver.get_P_load(),'W','-> type:',type(Receiver.get_P_load()))
    print(type(Receiver.get_P_load()))




