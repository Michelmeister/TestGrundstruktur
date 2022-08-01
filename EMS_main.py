# Author            Michel Meinert
# last modified     19.07.2022
                            ##### MELANI Energiemanagementsystem #####

#import sys
import time
#import struct
import threading
#import numpy as np

#import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.transaction import ModbusRtuFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus import exceptions
import constants as co
#import Gerätesteuerung_Obelix_Tesvolt_constants as tv
import Gerätesteuerung_Obelix_Tesvolt_modbus as tvmodbus
#import eigene Module:


class SunnyTripower(threading.Thread):
    def __init__(self, ipadr='134.169.132.230', port=502):          # Connection data of the battery-inverter
        self.client = ModbusClient(ipadr, port=port, timeout=0.8, strict=False)

    def connect(self, timeout=0.5):                                 # Connection establishment
        try:
            self.client.connect()
            print(self.client.connect())
        except IOError as err:
            print('Verbindungsfehler: ' + str(err))

    def disconnect(self):                                           # Disconnection
        try:
            self.client.close()
            print('Verbindung getrennt!')
        except IOError as err:
            print('Verbindungstrennung fehlgeschlagen: '+str(err))

    def get_SoC(self):
        try:                                    # (address, number of registers to read, kwargs)
            rr = self.client.read_input_registers(co.ID_SOC_BATT_U32_RO,2, unit=co.UNIT_ID2)
            decoder = BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return decoder.decode_32bit_int() / co.FIX1
        except exceptions.ModbusException as err:
            print(err)
            return (None)
# Defined Methods: connect, disconnect, get_SoC
