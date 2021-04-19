# Create Account & save Credentials to database
import json
import random
import requests
from telethon.tl.functions.account import UpdateProfileRequest

from config import api_key, api_id, api_hash
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio

from SmsPvaService import SmsPvaService
import time
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import JoinChannelRequest
from DBManager import DBManager

db_service = DBManager()
async def order_for_account():
    sms_service = SmsPvaService()
    data = sms_service.purchase_number()
    orderId = data['orderId']
    number = data['number']
    c_code = data['countryShortName']
    # Create Telegram Account
    client = TelegramClient( StringSession(), api_id=api_id, api_hash=api_hash,proxy=("socks5", '122.49.77.175', 3128) )
    await client.connect()
    print(number)

    if client.is_connected():
        try:

            code_req = await client.send_code_request( phone=number, force_sms=True )
            print( code_req )
            sms_code = sms_service.get_sms( c_code=c_code, order_id=orderId )
            print( sms_code )
            fname_list = ['🔥 97X Gems Leaked ✨','🔥 65X Coin Name Leaked ✨','🔥 Tesla buying 50BLN Worth of BTC ✨','🔥 37X Gems Leaked ✨']
            lname_list = ['👀','👀','👀','👀','👀' ]
            fname_pick_index = random.randint(0,len(fname_list) - 1)
            lname_pick_index = random.randint(0,len(lname_list) - 1)
            fname = fname_list[fname_pick_index]
            await client.sign_up( code=sms_code, first_name=fname, last_name=lname_list[lname_pick_index] )
            await client(UploadProfilePhotoRequest(
            await client.upload_file('dm_me.jpg')
            ))
            await client(UpdateProfileRequest(about='Insider Crypto Community  >> t.me/cryptoinsiderslimited  << (Exclusive Early Leaks)'))

            client_session = client.session.save()
            print( client_session )
            await client.send_message( '@vrushangdev', "Good Morning Sir" )
            await client(JoinChannelRequest('@cryptoinsiderslimited'))
            await client(JoinChannelRequest('@monkpy'))
            db_service.set_clients(phone_number=number, client_session=client_session, used_before= 0)
        except Exception as e:
            print(e)
            pass



loop = asyncio.get_event_loop()
loop.run_until_complete( order_for_account() )
# order_for_account()
