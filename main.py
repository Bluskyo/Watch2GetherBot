from discord import Intents, Client, Message
from responses import get_response
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN") #Gets token from .env file.

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

async def send_message(message, user_message):
    if not user_message:
        print("Intents are probably not enabled check dev dashboard.")
        return
    try:
        response = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f"{client.user} is now running!")
    
@client.event 
async def on_message(message):
    if message.author == client.user:
        return
        
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    #print(f"[{channel}] {username}: '{user_message}'")
    await send_message(message, user_message)
    
def main():
    client.run(token=token)

if __name__ == '__main__':
    main()