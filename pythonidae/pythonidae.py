# coding=utf-8


import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')
initial_extensions = ['cogs.documentation',
                      'cogs.members',
                      'cogs.owner',
                      'cogs.games',]


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:  # pylint: disable=broad-except
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')


bot.run(TOKEN, bot=True, reconnect=True)
