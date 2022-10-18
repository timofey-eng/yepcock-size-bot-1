from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, User
import csv
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")

client = TelegramClient(phone, api_id, api_hash)

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

print('Choose a group to scrape members from:')
i = 0
target_group = None
for g in groups:
    if g.id == 1173473651:
        target_group = g
        break
    print(str(i) + '- ' + g.title + ', id: -100' + str(g.id) + ', access_hash: ' + str(g.access_hash))
    i += 1

print('Fetching Members...')
all_participants = client.get_participants(target_group, aggressive=False)


def full_name(user) -> str:
    if user.last_name:
        return f'{user.first_name} {user.last_name}'
    return user.first_name

print('Saving In file...')
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
    lines_count = 0
    for idx,  user in enumerate(all_participants):
        print(full_name(user))
        if lines_count == 50:
            break
        username = ""
        if user.username:
            if user.username == 'Cake_stream':
                print('is cake, continue')
                continue
            username = user.username
        else:
            continue
        writer.writerow([username, user.id, user.access_hash, target_group.title, target_group.id])
        lines_count = lines_count + 1
print('Members scraped successfully.')
