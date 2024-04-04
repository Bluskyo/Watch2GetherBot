import requests
import json

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
                return link
            else:
                return "Error:", response.text

def get_response(message):
    p_message = message.lower()

    if "!w2" in p_message:
        return createW2Room(p_message)
    
    if "!help" in p_message:
        return "Use the ```!w2 (optional youtube link)``` command to create a room automatically :sunglasses:"