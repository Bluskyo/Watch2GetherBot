from discord import Intents, Client, Message
from responses import get_response
import os
from dotenv import load_dotenv

from methods.queue import addToQueue
from methods.roomCheck import runRoomCheck
from responses import rooms

load_dotenv()
token = os.getenv("DISCORD_TOKEN") #Gets token from .env file.
apiKey = os.getenv("W2APIKEY") 

intents = Intents.default()
intents.message_content = True
intents.message_content = True
intents.reactions = True 
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is now running!")

async def send_message(channel, content):
    try:
        await channel.send(content)
    except Exception as e:
        print(e)
    
@client.event 
async def on_message(message):
    if message.author == client.user:
        return
    user_message = message.content

    await send_message(message.channel, get_response(user_message))

@client.event 
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "🚀":
        guild = client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        runRoomCheck(rooms)
        if len(rooms) > 0:
            try:
                await send_message(channel, f'"{addToQueue(apiKey, rooms, message.content)}" added to queue! :rocket:')
            except IndexError:
                await send_message(channel,f"Could not find the video! :scream:")
        else:
            print(f"No active rooms found! Currently active rooms: {len(rooms)}")

def main():
    client.run(token=token)

if __name__ == '__main__':
    main()