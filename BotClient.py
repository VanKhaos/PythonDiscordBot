import asyncio
import discord
import config.discord_config as d_config
from discord.utils import get
from discord.ext import commands
from datetime import datetime

# Extension Import
initial_extensions = ['cogs.members', 'cogs.owner', 'cogs.levelsystem']

delta = datetime.now()
now = delta.strftime("%d.%m.%Y %H:%M:%S")


# Define Prefix for Channel & DM
def get_prefix(bot, message):
    # Command Prefix

    prefixes = ['!', '.']
    # Command Prefix for DM
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description=d_config.bot_description)

# Extension Load [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f'{now} | Loaded Extension: {extension}')
        except Exception as error:
            print(f'{now} | ERROR: {extension} cannot be loaded. [{error}]')


# Bot OnReady Event
@bot.event
async def on_ready():
    print(f'{now} | Logged in as: {bot.user.name} - {bot.user.id}\n')
    print(f'{now} | Discord Version: {d_config.discord_version}\n')
    print(f'{now} | Successfully logged in and booted...!\n')

    for server in bot.guilds:
        print(server.name)

    bot.loop.create_task(status_task())


# Bot Status Event
async def status_task():
    while True:
        activity = discord.Activity(name='sich hier mal um', type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(5)
        activity2 = discord.Activity(name='mit Bits und Bytes', type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity2)
        await asyncio.sleep(5)
        activity3 = discord.Activity(name='euch', type=discord.ActivityType.listening)
        await bot.change_presence(activity=activity3)
        await asyncio.sleep(5)



# Command Listner
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    servername = message.guild.name
    author = message.author
    content = message.content
    channel = message.channel
    print(f'{now} | {servername} - {channel} - {author}: {content}')
    await bot.process_commands(message)


bot.run(d_config.bot_token, bot=True, reconnect=True)
