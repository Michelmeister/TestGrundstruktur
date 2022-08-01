#!/usr/local/bin/python
# -*- coding: utf-8-*-


"""
Konstanten für das Programm des Wechselrichters "Sunny Tripower".
https://files.sma.de/downloads/STP60_SHP75_STPS60-SunSpec_Modbus-TI-de-14.pdf
"""

# ------------------------------ #
# File name: constants.py
# Author: Gian-Luca Di Modica
# Date created: 12.06.2018
# Date last modified: 20.03.2020
# Python Version: 3.7
# ------------------------------ #


"""Sunny Tripower"""
# Einstellungen
UNIT_ID1 = 125  # ID des Inverter Managers
UNIT_ID2 = 25 #ID des STP60
UNIT_ID3 = 200 #ID für Direktvermarkter


# Modbus-Datengrößen
READ_BUFFER_SIZE_OFFSET = 9
READ_BUFFER_SIZE_16 = 11
READ_BUFFER_SIZE_32 = 13
READ_BUFFER_SIZE_64 = 17
READ_BUFFER_SIZE_STR32 = 41
WRITE_BUFFER_SIZE = 12

# Formats
FIX0 = 1
FIX1 = 10
FIX2 = 100
FIX3 = 1000
FIX4 = 10000
FIX5 = -2

#Gateway UNITID = 125 mit Offset -1
ID_VERSION_NUM_U32_RO = 40044
ID_SERIAL_NUM_U32_RO = 40052
ID_DEVICE_CLASS_U32_RO = 40021
ID_TEMPERATURE_I16_RO = 40218
ID_STATUS_U16_RO = 40224
ID_P_INV_I16_RO = 40199
ID_DC_SPANNUNG_U16_RO = 40214
ID_UAC_L1N_U32_RO = 40195
ID_UAC_L2N_U32_RO = 40196
ID_UAC_L3N_U32_RO = 40197
ID_IAC_L1_U32_RO = 40188
ID_IAC_L2_U32_RO = 40189
ID_IAC_L3_U32_RO = 40190
ID_QAC_TOTAL_S32_RO = 40206
ID_Netzkopplung_E16_RW = 40347
ID_WMaxLimPct_I16_RW = 40348
ID_DC_LEISTUNG_I16_RO = 40216
ID_Leistungsfaktor_I16_RW = 40353
ID_Fester_Leistungsfaktor_E16_RW = 40358
ID_EinstellSpannung_U16_RO = 40271

#Control UNITID = 25, ohne Offset

ID_SOC_BATT_U32_RO = 1056
ID_BAT_TEMP_I32_RO = 1046
ID_SER_NO_U32_RO = 1000
ID_PAC_TOTAL_S32_RO = 1208
ID_Betriebsbefehl_I32_RW = 1400
ID_OpStt_I32_RO = 1004
ID_WIRKLEISTUNG_I16_RW = 40023
ID_FstStop_U32_RW = 40018

#UnitID = 200



