import discord
from discord.ext import commands
import os
import config as config

# Enable intents for the bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

# Initialize bot with intents
client = commands.Bot(command_prefix='$', intents=intents)

# Remove the default help command
client.remove_command('help')

# Load command modules synchronously
def load_extensions():
    for filename in ["mute", "unmute", "ping", "server_info", "bot_help"]:
        client.load_extension(f'commands.{filename}')

@client.event
async def on_ready():
    load_extensions()  # Load extensions when the bot is ready
    print(f'Logged in as {client.user}!')

# Run the bot
client.run(config.TOKEN)

