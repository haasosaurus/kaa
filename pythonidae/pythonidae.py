#!/usr/bin/env python
# coding=utf-8


#---------------------------- ideas ----------------------------#
# implement catching Ctrl+c so that the bot can be shutdown
# well and save the settings after conversion to use json
#
# switch print_context to use logging module
#
# fix packaging
#
# make method to call routines from coroutines
#---------------------------------------------------------------#


import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from pythonbot import PythonBot


def main() -> None:
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot = PythonBot()
    bot.run(token, bot=True, reconnect=True)


if __name__ == '__main__':
    main()
