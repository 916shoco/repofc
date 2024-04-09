import random
from pypresence import Presence
import time
# client_id = 1138194830846070815
RPC = Presence("1138194830846070815")
RPC.connect()

print("it's executed")
large_text_ = ["Watching Shadow Realm", "Faster n Harder", "I dont have any time for you", "Staring at you", "Stalking you"]
group_names = ["Shadow Realm", "I still miss him", "12/10"," have a bad day? tomorrow will be worse"]

while True:
    RPC.update(
        large_image= "https://th.bing.com/th/id/OIP.3IoGgV6nHodapKs4iJChMwHaJQ?w=190&h=238&c=7&r=0&o=5&dpr=1.2&pid=1.7",
        large_text= "Yuuki Makoto",
        details= random.choice(large_text_) ,
        state= "Join the group to talk with me",
        start= int(time.time()), #time elapse
        buttons= [{"label": random.choice(group_names) ,"url": "Your_Url"},{"label": "_Instagram_","url": "Your_Url"}] #buttons that will redirect user to those url
                        )
    
    time.sleep(70)