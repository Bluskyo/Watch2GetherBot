import requests
import os
from googleapiclient.discovery import build

def fetchVideoDetails(ytLink):
    apiKey = os.getenv("YTAPIKEY") 

    youtube = build('youtube', 'v3', developerKey=apiKey)

    #Gets videoID from link.
    videoId = ytLink[32:]

    # Request video details
    videoResponse = youtube.videos().list(
        part='snippet',
        id=videoId
    ).execute()

    videoTitle = videoResponse['items'][0]['snippet']['title']
    videoThumbnail = videoResponse['items'][0]['snippet']['thumbnails']["high"]["url"]

    return [videoTitle, videoThumbnail]

def addToQueue(apiKey, rooms, link): #Returns string
    URL ="https://api.w2g.tv/rooms/" + rooms[-1][0] + "/playlists/current/playlist_items/sync_update" #gets last room made.

    videoInfo = fetchVideoDetails(link)

    data = {
        "w2g_api_key": apiKey,
        "add_items": [{"url": link, "title": videoInfo[0], "thumb": videoInfo[1]}]
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