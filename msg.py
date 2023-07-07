import discord

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")

    # Get the channel ID
    channel_id = "1126540413466058812"

    # Get the channel
    channel = client.get_channel(1126540413466058812)

    # Check if the channel exists
    if channel is None:
        print("Channel does not exist")
    else:
        # Send a message to the channel
        await channel.send("Hello, world!")

client.run("MTEyNjUzMTA3MjMxOTA0MTU5Nw.GBkMSk.ogI24pZ9RRv6d2qZWrt1SO96mEaLqoqOKxG0I4")


# import discord

# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True
# intents.members = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print("Bot is ready!")

#     # Get all channels in the server
#     channels = client.get_all_channels()

#     # Print the channel IDs
#     for channel in channels:
#         print(channel.id)

# client.run("MTEyNjUzMTA3MjMxOTA0MTU5Nw.GBkMSk.ogI24pZ9RRv6d2qZWrt1SO96mEaLqoqOKxG0I4")
