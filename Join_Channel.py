import json
import random
import requests
import time
from telethon.errors import UserDeactivatedError
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from config import api_key, api_id, api_hash
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio
import csv, sys
from DBManager import DBManager
db_service = DBManager()
from telethon.tl.functions.messages import AddChatUserRequest, GetDialogsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPeerEmpty


def join_channels(target_channel):
    clients = db_service.get_clients()
    for client_session in clients:
        print(client_session[1])
        try:
            tg_client = TelegramClient( StringSession(str(client_session[1])), api_id=api_id, api_hash=api_hash )
            tg_client.connect()
            tg_client(JoinChannelRequest(target_channel))
            print(tg_client.get_me())
        except:
            db_service.update_client( client_session[1] )
            pass
join_channels("t.me/cryptoinsiderslimited")