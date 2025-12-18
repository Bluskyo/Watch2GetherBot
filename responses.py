import os
from datetime import datetime
from dotenv import load_dotenv

from methods.createRoom import createRoom
from methods.roomCheck import runRoomCheck
from methods.queue import addToQueue
from roomState import rooms

load_dotenv()
apiKey = os.getenv("W2G_API") 

def get_response(message):
    p_message = message.strip()

    if "!q" in p_message[:2]:
        if "https://" in p_message:
            if rooms:
                videoTitle = addToQueue(apiKey, rooms, p_message[3:])
                return f'"{videoTitle}" added to queue! :rocket:'
            else:
                link = createRoom(apiKey, rooms, p_message)
                linkToAdd = addToQueue(apiKey, rooms, p_message[3:])
                return f"No active rooms found! :scream:\nHere's a new room for you :face_holding_back_tears::sparkles: {link}\n'{videoTitle}' added to queue!"
        else:
            return f"\n'{p_message}' does not contain a link! :sneezing_face:"

    if "!w2 c" in p_message.lower():
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
                    roomsURL.append(f"{index + 1}. https://w2g.tv/rooms/{streamKey[0]} ({streamKey[1].strftime('%m/%d : %H:%M')}) <- Using this room!")
                else: 
                    roomsURL.append(f"{index + 1}. https://w2g.tv/rooms/{streamKey[0]} ({streamKey[1].strftime('%m/%d : %H:%M')})")
                index += 1
            return "\n".join(str(url) for url in roomsURL)
        else:
            return "No rooms made! Try !w2 to make a room!"

    if "!w2 set" in p_message.lower():
        try:
            index = int(p_message[8:]) - 1
            rooms.append(rooms[index])
            rooms.pop(index)
            return f"New current room set to: https://w2g.tv/rooms/{rooms[-1][0]}"
        except ValueError:
            return "Index has to be a whole number! :nerd: "

    if "!w2" in p_message.lower():
        if len(p_message) > 3 and p_message[4:12] != "https://":
            return None
        else:
            return createRoom(apiKey, rooms, p_message)

    if "!help" in p_message.lower():
        return "```!w2 <optional Youtube link> 'Creates a room.'```\
            ```!q <link> or 🚀 reaction 'Adds a video to the room.'```\
             ```!w2 c 'Shows the room being currently used.'``` \
             ```!w2 ls 'Shows a list of all available rooms.'``` \
             ```!w2 set <Room number> 'Changes the main room to the specified room.'```"
    
    if "!ver" in p_message.lower():
        return "Version: 2.0.1 🐳"