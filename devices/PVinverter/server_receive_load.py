import socket, errno, sys
import time
from threading import Thread
import struct


class Recheneinheit():
    def __init__(self,name):
        self.name = name
        #super().__init__()

    def connection(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket will create with TCP and IP protocols
            s.bind(('0.0.0.0', 42424))  # This method will bind the sockets with server and port no
            s.listen(100)  # Will allow a maximum of one connection to the socket
            print('Warte auf Verbindung')
            c, addr = s.accept()  # will wait for the client to accept the connection
            print("CONNECTION FROM:", str(addr))  # Will display the address of the client

# server
    def receive_load(self):
        try:


            msg = c.recv(1024)
            P_soll = float(msg.decode())
            print('P =',P_soll,'-> type:',type(P_soll))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return P_soll
        except socket.error as err:
            print('SocketError', str(err))
            pass
        except ConnectionResetError:
            print('ConnError')
            pass
        #return P_soll
        #time.sleep(0.5)

    def run(self):
        while True:
            print(self.receive_load(),type(self.receive_load()))


if __name__ == '__main__':

    RE = Recheneinheit('TestRE')
    print(RE.receive_load(),type(RE.receive_load()))



