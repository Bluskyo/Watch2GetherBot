import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("W2APIKEY") 

def createW2Room(rooms, ytlink="none"): #returns string link
    url = "https://api.w2g.tv/rooms/create.json"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    payload = {
        "w2g_api_key": apiKey,
        "share": ytlink,
        "bg_color": "#000000",
        "bg_opacity": "50"
    }

    json_payload = json.dumps(payload)

    response = requests.post(url, headers=headers, data=json_payload)

    if response.status_code == 200:
        data = response.json()

        link = f"https://w2g.tv/rooms/{data['streamkey']}"
        dateMade =  datetime.today() #Save room with timestamp. 
        roomInfo = (data['streamkey'], dateMade)

        today = datetime.today()
        index = 0

        if len(rooms) > 0:
            for i in rooms:
                delta = today - i[1]
                if delta.days >= 1:
                    rooms.pop(index)
                    
        rooms.append(roomInfo)
        print(rooms)
        return link
    else:
        return "Error:", response.text