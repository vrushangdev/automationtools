# Buy Number & Get OTP
from config import BAL_URL
import json
import requests
import random
import time


class SmsPvaService:
    service_price_url = None
    balance_url = None
    number_url = "http://smspva.com/priemnik.php?metod=get_number&country=COUNTRY_CODE&service=opt29&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"
    sms_url = "http://smspva.com/priemnik.php?metod=get_sms&country=COUNTRY_CODE&service=opt4&id=ORDER_ID&apikey=PuaVUbp3pkT3rSsuvuJNCH4NWTrILP"

    def __init__(self):
        self.balance_url = BAL_URL

    def get_price(self, service_price_url):
        """Get Price From SMS PVA"""
        response = requests.get( url=service_price_url )
        data = json.loads( response.text )
        # print(data['price'])
        return data['price']

    def get_balance(self):
        response = requests.get( url=self.balance_url )
        data = json.loads( response.text )
        print( data['balance'] )
        return data['balance']

    def select_country(self):
        try:
            handle = open( 'affordable_country.txt', 'r' )
            text = handle.read()
            handle.close()
            data = json.loads( text )
            pick = random.randint( 0, len( data ) )
            country = data[pick]
            return country['country']

        except Exception as e:
            print( "Exception opening file", e )

    def purchase_number(self):
        """Purchase number from smspva"""
        country = self.select_country()
        print( country )
        url = self.number_url.replace( "COUNTRY_CODE", str( country ) )
        resp = requests.get( url )
        print(resp)
        data = json.loads( resp.text )
        while data['number'] is None:
            country = self.select_country()
            print( "Trying A new Country .... Number Not Found" )
            print( country )
            url = self.number_url.replace( "COUNTRY_CODE", str( country ) )
            resp = requests.get( url )
            data = json.loads( resp.text )
            time.sleep( 5 )

        required_data = {'countryShortName': country, 'orderId': data['id'],
                         'number': data['CountryCode'] + " " + data['number']}
        print( data )
        print( required_data )
        return required_data

    def get_sms(self, c_code, order_id):
        """Get Sms From SmsPVA Service."""
        url = self.sms_url.replace( "COUNTRY_CODE", c_code ).replace( "ORDER_ID", str( order_id ) )
        resp = requests.get( url )
        data = json.loads( resp.text )
        print( data )
        while data['sms'] is None:
            resp = requests.get( url )
            print( resp.text )
            data = json.loads( resp.text )
            print( "Waiting for SMS..." )
            time.sleep( 5 )
        return data['sms']

# sms_service = SmsPvaService()
#
# order = sms_service.purchase_number()
# sms = sms_service.get_sms(order['countryShortName'], order['orderId'])
# print(sms)
