#!/usr/bin/env python
# coding=utf-8


import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print(f'discord.py version: {discord.__version__}')
    print('Servers:')
    for guild in bot.guilds:
        print(f'    Name: {guild.name}, Id: {guild.id}')


def load_extensions(bot):
    initial_extensions = [
        'cogs.documentation',
        'cogs.members',
        'cogs.owner',
        'cogs.games',
        'cogs.resources',
        'cogs.troll',
    ]
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:  # pylint: disable=broad-except
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


def main(bot):
    load_extensions(bot)
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token, bot=True, reconnect=True)


if __name__ == '__main__':
    main(bot)
