import requests
import json
import sqlite3
import Forecast_SQL
from datetime import datetime, timezone
import pandas as pd
import ast
import pytz


#-------------------------#
# File Name: NaturstromAPI.py
# Author: Marcel Luedecke
# Date created: 26.01.2023
# Date last modified: 26.01.2023
# Python Version: 3.9
#-------------------------#

#Test der Handelsparameter grade nicht möglich

class NaturstromAPI:

    #EnergyData

    def get_api_energydata_GetCurrentByHousingUnitId():
#Test funktioniert aktuell nur für Id1, nicht für Id0; Vorgabe von UnitID und addSiteDate als Bool in Query!"""

        url = "https://webservice.naturstrom.de:55008/api/energydata/GetCurrentByHousingUnitId?id=1&addSiteDate=false"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_api_energydate_GetCuurentBySite():
        #'''Klappt noch nicht'''

        url = "https://webservice.naturstrom.de:55008/api/energydata/GetCurrentBySite"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_api_energydata_GetDealsByHousingUnit():
        #'''Klappt noch nicht'''

        url = "https://webservice.naturstrom.de:55008/api/energydata/GetDealsByHousingUnit?dealsSelling=true&dealsBuying=true"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_api_energydata_Create_Deal():
        #'''Klappt noch nicht'''

        url = "https://webservice.naturstrom.de:55008/api/energydata/CreateDeal?tranche=1"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)


    def get_api_energydata_DeleteDeal():
        #'''Klappt noch nicht'''

        url = "https://webservice.naturstrom.de:55008/api/energydata/DeleteDeal"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_api_energydata_GetCurrentMultipliplicationFactorByHousingUnit():
        #Form des Datums?
        url = "https://webservice.naturstrom.de:55008/api/energydata/GetCurrentMultiplicationFactorByHousingUnit?housingUnitId=4&factorTime=2023-01-16T13%3A00%3A00"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def get_api_energydata_GetCurrentMultiplicationFactors():
        #'''klappt, gibt aktuell leeres Tuple zurück'''

        url = "https://webservice.naturstrom.de:55008/api/energydata/GetCurrentMultiplicationFactors"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
   #--------------------------------------------------------------------------------------#
    #'''Housing Units'''
    def get_api_housingunits_ping():
        '''Funktioniert vermutlich, gibt Pong zurück'''
        url = "https://webservice.naturstrom.de:55008/api/housingunits/ping"

        payload = ""
        headers = {
         'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_api_housingunits_GetAll():
        url = "https://webservice.naturstrom.de:55008/api/housingunits/GetAll"

        payload = ""
        headers = {
         'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def get_housingunits_Get():
        url = "https://webservice.naturstrom.de:55008/api/housingunits/Get?id=1"

        payload = ""
        headers = {
        'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def post_api_housingunits_Create():


        url = "https://webservice.naturstrom.de:55008/api/housingunits/Create?unitName=WE02"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def post_api_housingunits_Update():
        #bspw. UnitID oder Name über query anpassbar über Update
        url = "https://webservice.naturstrom.de:55008/api/housingunits/Update?id=4&unitName=WE02"

        payload = ""
        headers = {
            'token': 'DrOubmybFLMXguwjYpGCiUSufW5pDbgN1CiAfUwIt15MgNYtfRNnJgvRIupoqiGD'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)




NaturstromAPI.get_api_housingunits_GetAll()
