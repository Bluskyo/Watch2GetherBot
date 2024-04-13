import requests
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("W2APIKEY") 

def addToQueue(rooms, link): #Returns string
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