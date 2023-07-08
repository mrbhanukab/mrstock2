import requests
import json
import discord
from discord.ext import commands
from discord import Intents
from bs4 import BeautifulSoup
import os

# Function to format the name
def format_name(name):
    name = name.replace('.', '-')
    name = name.replace('(', '')
    name = name.replace(')', '')
    return name

# Bot setup
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load sensitive information from info.json
with open('info.json', 'r') as info_file:
    info = json.load(info_file)

TOKEN = info['TOKEN']
GUILD_ID = info['GUILD_ID']
CATEGORY_NAME = info['CATEGORY_NAME']
SETTING_ID = info['SETTING_ID']

# Load existing data from JSON file
existing_data = []
try:
    with open('output.json', 'r') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    pass

# Set of names already present in the JSON file
existing_names = set(item['name'] for item in existing_data)

# List to store the extracted data
data = []

# URLs to scrape
urls = [
    'https://www.marketwatch.com/tools/markets/stocks/country/sri-lanka/1',
    'https://www.marketwatch.com/tools/markets/stocks/country/sri-lanka/2'
]

# Scrape each URL
for url in urls:
    print(f'⌛ Scraping Data from {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags inside the table
    table = soup.find('table', class_='table')
    rows = table.tbody.find_all('tr')

    for row in rows:
        # Extract the link and name
        link = row.find('a')['href']
        name = row.find('small').get_text()

        # Format the name
        name = format_name(name)

        # Check if the name already exists in the JSON file
        if name in existing_names:
            continue

        # Create a dictionary with the link and formatted name
        item = {
            'link': f'https://www.marketwatch.com{link}',
            'name': name,
            'description': 'No description',
            'channel_id': None,
            'group_created': False
        }

        # Follow the link and extract the description
        inner_response = requests.get(item['link'])
        inner_soup = BeautifulSoup(inner_response.content, 'html.parser')
        description_element = inner_soup.find('p', class_='description__text')
        if description_element:
            item['description'] = description_element.get_text()

        # Add the item to the data list
        data.append(item)
        print(f"✅ Data Added: {name}")

# Combine existing data and new data
all_data = existing_data + data

# Write the updated data to the JSON file
with open('output.json', 'w') as file:
    json.dump(all_data, file, indent=4)

JSON_FILE_PATH = 'output.json'

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    if guild is not None:
        await create_channels(guild)
        await send_message_to_settings(guild, "⚠️ ```update.py``` started running")
        print("⚠️ update.py started running")

    # Stop the bot after execution
    os._exit(0)


async def create_channels(guild):
    with open(JSON_FILE_PATH) as file:
        data = json.load(file)

    categories = {}

    for entry in data:
        name = entry['name']
        category_letter = name[0].upper()
        category_name = f'Huuto ({category_letter})'

        if category_name not in categories:
            categories[category_name] = await get_or_create_category(guild, category_name)

        category = categories[category_name]

        if entry['group_created']:
            continue

        await create_text_channel(category, name, entry)
        await send_message_to_settings(guild, f'New group created: **{name}** ✅')
        print(f'New group created: {name} ✅')

    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


async def get_or_create_category(guild, category_name):
    for category in guild.categories:
        if category.name == category_name:
            return category

    return await guild.create_category(category_name)


async def create_text_channel(category, channel_name, entry):
    existing_channels = [ch.name for ch in category.channels]
    if channel_name not in existing_channels:
        channel = await category.create_text_channel(channel_name)
        entry['channel_id'] = channel.id
        entry['group_created'] = True

        # Set the description as the channel topic
        await channel.edit(topic=entry['description'])


async def send_message_to_settings(guild, message):
    setting_channel = guild.get_channel(SETTING_ID)
    if setting_channel is not None:
        await setting_channel.send(message)


bot.run(TOKEN)
