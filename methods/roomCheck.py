from datetime import datetime

def runRoomCheck(roomList): #Checks for rooms older then 1 day and deletes them from list.
    today = datetime.today()
    index = 0
    
    if len(roomList) > 0:
        for i in roomList:
            delta = today - i[1]
            if delta.days >= 1:
                roomList.pop(index)
        return roomList
    return roomList