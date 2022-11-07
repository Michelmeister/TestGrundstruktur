  def receive_load(self):
    try:
      s = socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)              # Socket will create with TCP and, IP protocols
      s.connect(('134.169.132.207', 42424))   # Will connect with the server
      msg = s.recv(1024)               # Will receive the reply message string from the server at 1024 B
      #while msg:
      P_soll = float(msg.decode())
      print('P_load =', P_soll, 'W =', P_soll / 1000, 'kW')  # fl
      #time.sleep(0.1) # ACHTUNG -> WERT DARF NICHT GRÖSSER SEIN ALS BEI SENDER
      #msg = s.recv(1024)  # Will run as long as the message string is empty
      s.close()
