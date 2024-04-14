import requests
import os
from googleapiclient.discovery import build

def fetchVideoDetails(ytLink):
    apiKey = os.getenv("YTAPIKEY") 

    youtube = build('youtube', 'v3', developerKey=apiKey)

    #Gets videoID from link.

    videoId = ""

    urlParts = ytLink.split("/")

    if urlParts[2] == "www.youtube.com" or urlParts[2] == "m.youtube.com" :
        idAndParam = urlParts[3].split("=")
        if len(idAndParam[1]) == 11:
            videoId = idAndParam[1]
        else:
            vidID = idAndParam[1].split("&")
            videoId = vidID[0]

    elif urlParts[2] == "youtu.be":
        idAndParam = urlParts[3].split("?")
        if len(idAndParam) == 11:
            videoId = idAndParam[0]

    # Request video details
    videoResponse = youtube.videos().list(
        part='snippet',
        id=videoId
    ).execute()

    if len(videoId) != 11:
        return [ytLink, ytLink]

    videoTitle = videoResponse['items'][0]['snippet']['title']
    videoThumbnail = videoResponse['items'][0]['snippet']['thumbnails']["high"]["url"]

    return [videoTitle, videoThumbnail]

def addToQueue(apiKey, rooms, link): #Returns string
    URL ="https://api.w2g.tv/rooms/" + rooms[-1][0] + "/playlists/current/playlist_items/sync_update" #gets last room made.

    videoInfo = fetchVideoDetails(link)

    if "www.youtube.com" in videoInfo[1]:
        data = {
        "w2g_api_key": apiKey,
        "add_items": [{"url": link, "title":link}]
    }
    else:
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