import csv
import sys
import time
import struct
from threading import Thread
import numpy as np
from datetime import datetime
import socket
import time

# from Broadcast import Broadcast

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus import exceptions
#import laboratory.DCquelle.constants as co
import laboratory.DCquelle.constants_EA91000 as coDC
import laboratory.DCquelle.EA91000 as dc
import socket
import numpy as np
import xlsxwriter
import pandas as pd
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer


class DCquelle(Thread):
    def __init__(self, ipadr, port=5025, framer=ModbusRtuFramer):
        super().__init__()
        self.client = ModbusClient(ipadr, port, timeout=0.8, framer=ModbusRtuFramer, strict=False)
        self.ipadr = ipadr

    def connect(self):
        try:
            self.client.connect()
            print(self.client.connect())
        except:
            'Keine Verbindung'

    def disconnect(self):
        try:
            self.client.close()
            # print(self.client.close())
        except:
            'Fehler beim Verbindungsabbau!'



    def get_nennspannung(self):
        try:
            rr = self.client.read_holding_registers(
                address=121, count=2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return decoder.decode_32bit_float()

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_nennstrom(self):
        try:
            rr = self.client.read_holding_registers(
                address=123, count=2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return decoder.decode_32bit_float()

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_nennleistung(self):
        try:
            rr = self.client.read_holding_registers(
                address=125, count=2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return decoder.decode_32bit_float()

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    # %% eingestellte Sollwerte ablesen
    def get_uSoll(self):
        try:
            rr = self.client.read_holding_registers(
                address=500, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round((decoder.decode_16bit_uint() * self.get_nennspannung()) / 52428)

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_iSoll(self):
        try:
            rr = self.client.read_holding_registers(
                address=501, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round((decoder.decode_16bit_uint() * self.get_nennstrom()) / 52428)

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_pSoll(self):
        try:
            rr = self.client.read_holding_registers(
                address=502, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round((decoder.decode_16bit_uint() * self.get_nennleistung()) / 52428)

        except exceptions.ModbusException as err:
            print(err)
            return (None)
        # %%  Sollwerte setzen

    def set_uSoll(self, u):
        try:
            val_set = self.spg_float_to_uint(spg_float=u)
            rq = self.client.write_register(address=500, value=val_set)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def set_iSoll(self, i):
        try:
            val_set = self.strom_float_to_uint(strom_float=i)
            rq = self.client.write_register(address=501, value=val_set)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def set_pSoll(self, p: float):
        try:
            val_set = self.leistung_float_to_uint(leistung_float=p)
            rq = self.client.write_register(address=502, value=val_set)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def strom_float_to_uint(self, strom_float: float) -> int:
        return int(52428. * strom_float / self.get_nennstrom())

    def leistung_float_to_uint(self, leistung_float: float) -> int:
        return int(52428. * leistung_float / self.get_nennleistung())

    def spg_float_to_uint(self, spg_float: float) -> int:
        return int(52428. * spg_float / self.get_nennspannung())

    # %% IstWerte ablesen
    def get_uIst(self):
        try:
            rr = self.client.read_holding_registers(
                address=507, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round((decoder.decode_16bit_uint() * self.get_nennspannung()) / 52428, 2)

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_iIst(self):
        try:
            rr = self.client.read_holding_registers(
                address=508, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round(decoder.decode_16bit_uint() * self.get_nennstrom() / 52428, 2)

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    def get_pIst(self):
        try:
            rr = self.client.read_holding_registers(
                address=509, count=1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return round(decoder.decode_16bit_uint() * self.get_nennleistung() / 52428, 2)

        except exceptions.ModbusException as err:
            print(err)
            return (None)

    # %% Fernsteuerung-Modus ein, aus und ablesen
    def fernsteuerung_ein(self):
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                           wordorder=Endian.Big)
            # for x in treppe:
            builder.add_16bit_uint(0xFF00)
            rq = self.client.write_coil(402, 0xFF00)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def fernsteuerung_aus(self):
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                                           wordorder=Endian.Big)
            # for x in treppe:
            builder.add_16bit_uint(0x0000)
            rq = self.client.write_coil(402, 0x0000)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def check_fernsteuerung(self):
        rr = self.client.read_coils(address=402, count=1)
        if rr.bits[0] == True:
            print('Fernsteuerungsmodus: Ein')
        else:
            print('Fernsteuerungsmodus: Aus')

    # %% DC-Ausgang ein- und ausschalten
    def DC_ein(self):
        print('STARTE PV-ERZEUGUNG!')
        try:
            rq = self.client.write_coil(405, 0xFF00)
            return rq

        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def DC_aus(self):
        print('ENDE PV-ERZEUGUNG!')
        try:
            rq = self.client.write_coil(405, 0x0000)
            return rq
        except (exceptions.ModbusException, exceptions.ModbusIOException,
                TypeError, Exception) as err:
            print(err)
            return None

    def check_DC(self):
        rr = self.client.read_coils(address=405, count=1)
        if rr.bits[0] == True:
            print('DC-Ausgang: Ein')
        else:
            print('DC-Ausgang: Aus')

    def set_sollwerte(self, u, i, p, t):
        self.fernsteuerung_ein()
        self.set_uSoll(u)
        self.set_iSoll(i)
        self.set_pSoll(p)
        print('u_soll= ', self.get_uSoll(), ', i_soll= ', self.get_iSoll(), ', p_soll=',
              self.get_pSoll())
        self.DC_ein()
        for i in range(t):
            time.sleep(1)
            print(datetime.now(), ', u_ist= ', self.get_uIst(), ', i_ist= ', self.get_iIst(), ', p_ist= ',self.get_pIst())
            self.get_pIst()
        self.DC_aus()

    def DC_dynamisch(self, u, i):
        csv_file = open('C:/Users/eelab.ELENIA/Desktop/MELANI/laboratory/DCquelle/CSV.PV/Sunny_06bis18Uhr_2021Jun17.csv',newline='')
        PVgeneration = csv.DictReader(csv_file,delimiter=';')
        self.fernsteuerung_ein()
        self.set_uSoll(u)
        self.set_iSoll(i)
        p = 0
        self.set_pSoll(p)
        self.DC_ein()

        for row in PVgeneration:
            try:
                if row['Einstrahlung'] == '':
                    print('Ungültiger Wert, halte vorherigen Wert! -> P_pv =',p,'W -------> DC Quelle P_ist =',self.get_pIst(),'W')
                    time.sleep(1)
                elif row['Einstrahlung'] != '' and float(row['Einstrahlung']) < 15:
                    p = 0
                    self.set_pSoll(p)
                    print(row['Timestamp'], '-> G =', row['Einstrahlung'], 'W/m² -> P_pv =', p,'W -------> DC Quelle P_ist =', self.get_pIst(), 'W')
                    time.sleep(1)
                else:
                    PV_Peakleistung = 5 # kWp
                    p = round(float(row['Einstrahlung']) * PV_Peakleistung)
                    self.set_pSoll(p)
                    print(row['Timestamp'],'-> G =',row['Einstrahlung'],'W/m² -> P_pv =',p, 'W -------> DC Quelle P_ist =',self.get_pIst(),'W')
                    time.sleep(1)

            except KeyboardInterrupt:
                self.DC_aus()
                print('Verbindung manuell unterbrochen -> P_soll auf 0 gesetzt! -> Prüfe:',self.get_pIst(),'W =',self.get_pSoll())

        self.DC_aus()

    def run(self):
        self.DC_dynamisch(u=800, i=10)



if __name__ == '__main__':
    DC1 = DCquelle('134.169.132.167')
    DC1.connect()

    #print('Nennspannung: ', DC1.get_nennspannung())
    #print('Nennleistung: ', DC1.get_nennleistung())
    #print('Nennstrom: ', DC1.get_nennstrom())

    #DC1.run()
    DC1.DC_aus()

    DC1.fernsteuerung_aus()

    DC1.disconnect()



