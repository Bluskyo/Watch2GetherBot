from datetime import datetime
from datetime import datetime

def runRoomCheck(roomList):
    today = datetime.today()
    return [room for room in roomList if (today - room[1]).days < 1]