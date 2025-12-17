import requests
import os
import re
from googleapiclient.discovery import build

def fetchVideoDetails(ytLink):
    try:
        apiKey = os.getenv("YT_API")

        if apiKey:
            youtube = build('youtube', 'v3', developerKey=apiKey)
            findVideoID = re.search("[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]", ytLink)
            videoID = findVideoID.group() #Chooses string matched by regex.

            # Request video details
            videoResponse = youtube.videos().list(
                part='snippet',
                id=videoID
            ).execute()

            videoTitle = videoResponse['items'][0]['snippet']['title']
            videoThumbnail = videoResponse['items'][0]['snippet']['thumbnails']["high"]["url"]

            return [videoTitle, videoThumbnail]
        else:
            return [ytLink, ytLink]
    except AttributeError:
        print("Cant find details for: " + ytLink)
        return [ytLink, ytLink]
    
def addToQueue(apiKey, rooms, link): #Returns string
    URL ="https://api.w2g.tv/rooms/" + rooms[-1][0] + "/playlists/current/playlist_items/sync_update" #gets last room made.

    videoInfo = fetchVideoDetails(link)

    if "www.youtube.com" in videoInfo[1]:
        data = {
        "w2g_api_key": apiKey,
        "add_items": [{"url": link, "title":link}]
        }
        title = link
    else:
        data = {
            "w2g_api_key": apiKey,
            "add_items": [{"url": link, "title": videoInfo[0], "thumb": videoInfo[1]}]
        }
        title = videoInfo[0]

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url=URL, headers=headers, json=data)

    if response.status_code == 200:
        return title
    else:
        return "Error:", response.text