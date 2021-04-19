# 0. Select Client that is not used
# 1. Fetch all users from source & target group | find the difference
# 2. Add 30-50 unique people to our group | Mark Client used
# 4. Repeat & Select New Client

import json
import random
import requests
import time

from telethon.errors import UserDeactivatedError
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from config import api_key
# api_hash = "f130a32340a40482adf14858fe2ca3f9"
# api_id = "1482064"
api_hash = "0dfec003708fcd7e1e51fc48d9ddead4"
api_id = "3570489"
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio
import csv, sys
from DBManager import DBManager
db_service = DBManager()
from telethon.tl.functions.messages import AddChatUserRequest, GetDialogsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPeerEmpty, UserStatusOnline

target_group = 't.me/TrendMasterIndicator'
our_group = 't.me/cryptoinsiderslimited'

def select_client():
    clients = db_service.get_clients()
    pick_client_index = random.randint(0, len(clients) - 1)
    client_detail = clients[pick_client_index]
    client_session = client_detail[1]
    return client_session


async def add_people( client_session ):
    users = []
    members = []
    try:
        tg_client = TelegramClient( StringSession(str(client_session)), api_id=api_id, api_hash=api_hash)
        new_participants = []
        await tg_client.connect()
        await tg_client(JoinChannelRequest(target_group))
        if tg_client.is_connected():
            all_participants = await tg_client.get_participants(target_group, aggressive=True)
            our_participants = await tg_client.get_participants(our_group, aggressive=True)
            print(all_participants[0])
            for user in all_participants:
                if type(user.status) is UserStatusOnline:
                    if user.username is not None:
                        users.append(user)
            for person in our_participants:
                if person.username is not None:
                    members.append(person)
            n=0
            print(len(users))
            try:
                client_session = select_client()
                client = TelegramClient( StringSession(str(client_session)), api_id=api_id, api_hash=api_hash )
                print(len(users))
                for user in users:

                    await client.connect()
                    await client(JoinChannelRequest('t.me/TrendMasterIndicator'))
                    # user_to_add = await client.get_input_entity(user.username)
                    chats = await client(GetDialogsRequest(
                        offset_date=None,
                        offset_id=0,
                        offset_peer=InputPeerEmpty(),
                        limit=100,
                        hash=0))
                    channel = None
                    for chat in chats.chats:
                        if "Crypto Insiders" in chat.title:
                            channel = await client.get_entity(chat.id)
                            try:
                                await client(InviteToChannelRequest(channel, [user]))
                                time.sleep(1)
                                print("User Invited >>> ", user)
                            except Exception as e:
                               pass

            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        pass



client_session = select_client()

loop = asyncio.get_event_loop()

loop.run_until_complete( add_people(client_session) )