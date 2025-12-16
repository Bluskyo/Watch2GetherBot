# Watch2GetherBot
A Discord Bot for creating Watch2Gether rooms automatically, and adding videos to the the room through discord chat.

### Supported Commands: <br>
`!w2 <optional Youtube link>` : Creates a room.           
`!q <link> or 🚀 reaction` : Adds a video to room. <br>
`!w2 room / r / c ` : Shows the main room. <br>
`!w2 ls` : Shows a list of all available rooms. <br>
`!w2 set` : <Room number> Changes the main room to the specified room. <br>

### Demo
<img src="https://github.com/Bluskyfishing/Watch2GetherBot/assets/121456599/1d303e5f-6e5b-4d01-a65b-543f7e1cac6f" width="300" height="500">

## Getting Started
### API Keys and tokens
1. Create a .env file to safely store the api keys and bot token in the same directory as the dotfiles.
2. Go to https://discord.com/developers/applications to create a discord bot.
   This bot will need "Send message", "Read Message History" and "Add Reactions" permissions.
4. Go to https://w2g.tv/en/account/edit_user/ to get the watch2gether api key. (Requires an account).

<strong> Optional (Needed for fetching thumbnail images): </strong> <br>
Go to https://console.cloud.google.com/apis and make a "YouTube Data API v3" api key.

### Docker Container
1. Run `docker build -t w2bot:latest .` to create the image for the bot.
2. Then run `docker run -d --name w2bot_container w2bot:latest` to make and run the container.

The bot should now be running. To test it send "!w2" in a open text channel.
