import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("W2APIKEY") 

rooms = [] #Should contain tuple like = (link, date)

def createW2Room(ytlink="none"):
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

def addToQueue(link):
    URL ="https://api.w2g.tv/rooms/" + rooms[-1][0] + "/playlists/current/playlist_items/sync_update" #gets last room made.

    data = {
        "w2g_api_key": apiKey,
        "add_items": [{"url": link, "title": link}]
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url=URL, headers=headers, json=data)

    if response.status_code == 200:
        return "Video added to queue:exclamation:"
    else:
        return "Error:", response.text

def get_response(message):
    p_message = message

    if "!w2" in p_message.lower() and len(p_message) == 3:
        return createW2Room(p_message)
    
    if "!w2 room" in p_message.lower() or "!w2 r" in p_message.lower():
        if len(rooms) > 0:
            return "Currently using room: https://w2g.tv/rooms/" + rooms[-1][0]
        else:
            return "No rooms made! Try !w2 to make a room!"

    if "!w2 ls" in p_message.lower():
        if len(rooms) > 0:
            roomsURL = ["Currently active rooms:"]
            index = 0
            
            for streamKey in rooms:
                if index == len(rooms) - 1:
                    roomsURL.append(f"{index + 1}. https://w2g.tv/rooms/{streamKey[0]} <-- Current active room!")
                else: 
                    roomsURL.append(f"{index + 1}. https://w2g.tv/rooms/{streamKey[0]}")
                index += 1

            return "\n".join(str(url) for url in roomsURL)
        else:
            return "No rooms made! Try !w2 to make a room!"
    
    if "!w2 set" in p_message[:7].lower():
        try:
            index = int(p_message[8:]) - 1
            rooms.append(rooms[index])
            rooms.pop(index)
            return f"New current room set to: https://w2g.tv/rooms/{rooms[-1][0]}"
        except ValueError:
            return "Index has to be a whole number! :nerd: "

    if "!q" in p_message[:2]:
        return addToQueue(p_message[3:])
    
    if "!help" in p_message.lower():
        return "Use the ```!w2 (optional youtube link)``` command to create a room automatically :sunglasses: \n and use ```!q (link)``` to add a video to the queue!"