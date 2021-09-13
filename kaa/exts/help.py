# -*- coding: utf-8 -*-


# standard library modules
import asyncio
import datetime
import importlib
import io
import itertools
import json
import os
import pathlib
import random
import re
import traceback
from typing import List, Union

# third-party packages
import dateparser
import PIL
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import pytz

# third-party packages - discord related
import discord
from discord.ext import commands, tasks
import dislash
from dislash import ActionRow, Button, SelectMenu, SelectOption, ButtonStyle, slash_commands

# local modules
from kaa import Kaa
from utils import print_context
import kaa_help
from kaa_help import KaaHelp
import constants
from constants import Colors


class Help(commands.Cog, name='help'):
    """
    help commands
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot




    @commands.command(
        name='help_owner',
        aliases=['ho'],
        hidden=True,
    )
    @commands.is_owner()
    async def help_owner_command(self, ctx: commands.Context, *, args: str) -> None:
        """full help docs for owner"""

        self.bot.help_command = KaaHelp(owner=True)
        await ctx.send_help(args)
        self.bot.help_command = KaaHelp()




    @commands.command(
        name='default_help',
        aliases=['defaulthelp'],
        hidden=True,
    )
    @commands.is_owner()
    async def default_help_command(
            self,
            ctx: commands.Context,
    ) -> None:
        """
        set default help command
        """

        self.bot.help_command = commands.DefaultHelpCommand()




    @slash_commands.command(
        name='reload_help',
        description="reloads help command",
        guild_ids=[
            791589784626921473,  # ck
            864816273618763797,  # kaa
        ],
    )
    @slash_commands.is_owner()
    async def reload_help_slash(self, inter: dislash.SlashInteraction) -> None:
        """
        this slash command updates Kaa's help command to the current code
        """

        await self._reload_help()
        embed = discord.Embed(
            color=Colors.success,
        )
        name = 'Success'
        value = 'reloaded the help command code'
        embed.add_field(name=name, value=value, inline=False)
        await inter.reply(embed=embed)




    @commands.command(
        name='reload_help',
        aliases=['rh'],
        description='reloads help command',
        help="this command updates Kaa's help command to the current code",
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_help_command(self, ctx: commands.Context) -> None:
        """
        this command updates Kaa's help command to the current code
        """

        await self._reload_help()
        msg = 'reloaded the help command code'
        return await self.bot.send_success_msg(ctx, msg)




    async def _reload_help(self) -> None:
        """
        backend for reload_help_command and reload_help_slash
        """

        importlib.reload(constants)
        importlib.reload(kaa_help)
        self.bot.help_command = kaa_help.KaaHelp()









def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    importlib.reload(kaa_help)
    bot.add_cog(Help(bot))
