import requests
import json
from datetime import datetime

rooms = [] #Should contain tuple like = (link, date)

def createW2Room(ytlink="none"):
            url = "https://api.w2g.tv/rooms/create.json"

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            payload = {
                #"w2g_api_key": "<api-key>",
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

                rooms.append(roomInfo)

                return link
            else:
                return "Error:", response.text

def addToQueue(ytlink):
    URL ="https://api.w2g.tv/rooms/" + rooms[-1][0] + "/playlists/current/playlist_items/sync_update" #get last room made.

    PARAMS = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                #"w2g_api_key": "<api-key>",
                'add_items': [{'url': ytlink, 'title': 'Hello World'}]
            }
    response = requests.post(url= URL, params=PARAMS)

    if response.status_code == 200:
        return f"Added to queue! :exclamation:"
    else:
        return "Error:", response.text

def get_response(message):
    p_message = message.lower()

    if "!w2" in p_message:
        return createW2Room(p_message)
    
    if "!q" in p_message[:2]:
        return addToQueue(p_message[3:])
    
    if "!help" in p_message:
        return "Use the ```!w2 (optional youtube link)``` command to create a room automatically :sunglasses: \n and use ```!q (link)``` to add a video to the queue!"