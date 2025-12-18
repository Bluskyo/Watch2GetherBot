import time
import os
import discord
import asyncio

from discord import Intents, Client, Message
from dotenv import load_dotenv

from roomState import rooms
from responses import get_response
from methods.queue import addToQueue
from methods.roomCheck import runRoomCheck
from methods.createRoom import createRoom

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
apiKey = os.getenv("W2G_API")

intents = Intents.default()
intents.message_content = True
intents.message_content = True
intents.reactions = True 
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is now running!")
    await set_bot_status("!w2 to create a room!")

    while True:
        await asyncio.sleep(5)
        runRoomCheck(rooms)
        if (len(rooms) >= 1):
            await set_bot_status("w2g room is open! 🚪")
        else:
            await set_bot_status("!w2 to create a room!")

async def set_bot_status(text):
    game = discord.Game(text)
    await client.change_presence(status=discord.Status.online, activity=game)

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

        if "https://" in message.content:
            if rooms:
                videoTitle = addToQueue(apiKey, rooms, message.content)
                await send_message(channel, f'"{videoTitle}" added to queue! :rocket:')
            else:
                link = createRoom(apiKey, rooms, message.content)
                videoTitle = addToQueue(apiKey, rooms, message.content)
                await send_message(channel, f'No active rooms found! :scream:\nHeres a new room for you :face_holding_back_tears::sparkles: {link}\n"{videoTitle}" added to queue! :rocket:')
        else:
            await send_message(channel, f"\n'{message.content}' does not contain a link! :sneezing_face:")

def main():
    client.run(token=token)

if __name__ == '__main__':
    main()