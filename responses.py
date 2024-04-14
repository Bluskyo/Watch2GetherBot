from datetime import datetime
import os
from dotenv import load_dotenv

from methods.createRoom import createW2Room
from methods.queue import addToQueue

load_dotenv()
apiKey = os.getenv("W2APIKEY") 

rooms = [] #Should contain tuple like = (link, date)

def get_response(message):
    p_message = message

    if "!w2" in p_message.lower() and len(p_message) == 3:
        return createW2Room(apiKey, rooms, p_message)
    
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
        try:
            return addToQueue(apiKey, rooms, p_message[3:])
        except IndexError:
            return "Could not find link!:scream:"
    
    if "!help" in p_message.lower():
        return "```!w2 <optional Youtube link> 'Creates a room.'```\
            ```!q <link> 'Adds a video to room.'```\
             ```!w2 room 'Shows the main room.'``` \
             ```!w2 ls 'Shows a list of all available rooms.'``` \
             ```!w2 set <Room number> 'Changes the main room to the specified room.'```"