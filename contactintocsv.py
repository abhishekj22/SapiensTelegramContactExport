#from telethon import functions, types
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 1341306  #paste API ID here 
api_hash = '666f775ed259e0ffe680a7994f25bca0'  #paste API HASH here in quotes
phone = '+918828176706' #admin phone number (but as tested non admin number can also extract list)

##channel_username = 'https://t.me/testchnl4'

client = TelegramClient(phone, api_id, api_hash)

#connect client to telegram
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code/otp received: '))


chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i=0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i+=1

g_index = input("Enter a Group Number: ")
target_group=groups[int(g_index)]

print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
#all_participants = client.get_participants(channel_username, aggressive=True)

print('Saving In file intp csv format...')
with open("contactlList.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user_id','Name', 'Phone Number']) #remove if not needed username and user_id
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,name,user.phone])  #if remove from above please remove from here username and user.id
print('Members exported successfully!')



#with TelegramClient(name, api_id, api_hash) as 
#client:
#    result2 = client(functions.users.GetFullUserRequest(
#        id='abhishektest_bot'
#    ))
#    print(result2.stringify())