#!/usr/bin/env python
# coding=utf-8


import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='!')
# bot.remove_command('help')


# implement catching Ctrl+c so that the bot can be shutdown
# well and save the settings after conversion to use json


@bot.event
async def on_ready() -> None:
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    print(f'discord.py version: {discord.__version__}')
    print('Servers:')
    for guild in bot.guilds:
        print(f'    Name: {guild.name}, Id: {guild.id}')


def load_extensions(bot: commands.Bot) -> None:
    initial_extensions = [
        'cogs.documentation',
        'cogs.members',
        'cogs.owner',
        'cogs.games',
        'cogs.resources',
        'cogs.troll',
        'cogs.countdown',
        'cogs.listener',
        'cogs.memes',
        # 'cogs.help',
    ]
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except (
                commands.ExtensionNotFound,
                commands.ExtensionAlreadyLoaded,
                commands.NoEntryPointError,
                commands.ExtensionFailed
        ):
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


def main(bot: commands.Bot) -> None:
    load_extensions(bot)
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token, bot=True, reconnect=True)


if __name__ == '__main__':
    main(bot)
