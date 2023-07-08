import discord
import json

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

with open('info.json', 'r') as info_file:
    info = json.load(info_file)

TOKEN = info['TOKEN']
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")

async def send_message(channel_id, msg):
    channel = client.get_channel(channel_id)
    if channel is None:
        print("Channel does not exist")
    else:
        await channel.send(msg)

def start_bot():
    client.run(TOKEN)
