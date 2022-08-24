from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
token = os.getenv("TG_BOT_TOKEN")

client = TelegramClient(phone, api_id, api_hash)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

i = 0
target_group = None
for g in groups:
    if g.id == 1173473651:
        target_group = g
        break
    print(str(i) + '- ' + g.title + ', id: -100' + str(g.id) + ', access_hash: ' + str(g.access_hash))
    i += 1

# yepcocktest_size_bot bot_test_id = 5209727784
# yepcock_size_bot bot_test_id = 5209493476
# bot_id = await bot.get_me()
# print(str(bot_id))


messages = []


def get_messages():
    for message in client.iter_messages(target_group, limit=50, from_user='yepcock_size_bot', add_offset = 0):
        if message.sender_id == 5209493476:
            print(message.sender_id, ':', message.text, ':', message.id)
            messages.append(message)


async def delete_messages(messages):
    print('delete_messages called')
    for message in messages:
        print('try delete', ':', message.id)
        try:
            await bot.delete_message(chat_id=-1001173473651, message_id=message.id)
        except Exception as e:
            print(str(e))


async def delete_message(message_id):
    print('delete_message called')
    print('try delete', ':', message_id)
    await bot.delete_message(chat_id=-1001173473651, message_id=message_id)


def main():
    get_messages()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_messages(messages))
    # loop.run_until_complete(delete_message(646298))


if __name__ == '__main__':
    main()
