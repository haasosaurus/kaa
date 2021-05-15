#!/usr/bin/env python
# coding=utf-8


import asyncio
import copy
import json
import pathlib
import sys
import traceback
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

import discord
from discord.ext import commands

from pretty_help import PrettyHelp


class PythonBot(commands.Bot):
    """commands.Bot sublass, trying to clean things up around here"""

    def __init__(self) -> None:
        intents = discord.Intents.all()
        commands.Bot.__init__(
            self,
            command_prefix=PythonBot.prefixes_for,
            case_insensitive=True,
            help_command=PrettyHelp(),
            intents=intents,
        )
        self.settings = self.load_settings()
        self.load_extensions()
        self._owner = None
        self.message_counts = {}

    # test this to make sure it's using the cache
    @staticmethod
    async def prefixes_for(bot, message: discord.Message, guild_prefixes={}) -> Union[str, list]:
        """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

        # Only allow ! to be used in DMs, fix this up later
        if not message.guild:
            return '!'

        # get guild specific prefixes
        if message.guild.id not in guild_prefixes:
            prefixes = list(bot.settings['prefix_default'])
            for guild in bot.settings['guilds']:
                if bot.settings['guilds'][guild]['id'] == message.guild.id:
                    override = bot.settings['guilds'][guild].get('prefix_override', [])
                    if override:
                        prefixes = list(override)
                    prefixes += bot.settings['guilds'][guild].get('prefix_extra', [])
                    guild_prefixes.update({message.guild.id: prefixes})
                    break
        else:
            prefixes = list(guild_prefixes[message.guild.id])

        # get any custom user prefixes
        for user in bot.settings['users']:
            if bot.settings['users'][user].get('id', None) == message.author.id:
                custom_prefixes = bot.settings['users'][user].get('custom_prefixes', None)
                if custom_prefixes:
                    prefixes += custom_prefixes
                break

        return prefixes

    def load_settings(self) -> dict:
        """
        this just loads the setting file
        probably should make it just do an update on the
        settings dict with a user_settings.json file
        """

        settings_path = pathlib.Path('settings.json').resolve()
        if not settings_path.exists():
            print('ERROR: settings.json not found, exiting...')
            sys.exit()
        with settings_path.open('r') as settings_file:
            settings = json.load(settings_file)
        if settings.get('alt_settings_path', None):
            alt_settings_path = pathlib.Path(settings['alt_settings_path']).expanduser().resolve()
            if not alt_settings_path.exists():
                print(f"ERROR: alt settings file '{alt_settings_path}' doesn't exit, using default...")
            else:
                print(f"loading alt settings file '{alt_settings_path}'...")
                with alt_settings_path.open('r') as settings_file:
                    settings = json.load(settings_file)
        return settings

    def load_extensions(self) -> None:
        """load ethe extensions specified by the settings file"""

        for extension in self.settings['default_extensions']:
            try:
                self.load_extension(extension)
            except (
                    commands.ExtensionNotFound,
                    commands.ExtensionAlreadyLoaded,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed
            ):
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def get_owner(self) -> discord.User:
        """returns owner discord.User object, caches it for reuse"""

        if not self._owner:
            app_info = await self.application_info()
            self._owner = app_info.owner
        return self._owner

    async def get_guild_settings(self, obj: Union[str, discord.Member]) -> Optional[dict]:
        """returns dict of guild specific settings"""

        guild_id = None
        if isinstance(obj, str):
            for guild_settings in self.settings['guilds'].values():
                if guild_settings['nick'] == obj:
                    return copy.deepcopy(guild_settings)
            return None
        elif isinstance(obj, discord.Member):
            guild_id = obj.guild.id
        if not guild_id:
            return None
        for guild_settings in self.settings['guilds'].values():
            if guild_settings['id'] == guild_id:
                return copy.deepcopy(guild_settings)
        return None

    async def send_titled_msg(self, ctx: Union[commands.Context, discord.User], title: str, msg: str, color: int) -> None:
        embed = discord.Embed(
            color=color,
        )
        embed.add_field(
            name=title,
            value=msg,
            inline=False
        )
        return await ctx.send(embed=embed)

    async def send_untitled_msg(self, ctx: Union[commands.Context, discord.User], msg: str, color: int, thumbnail: str = None) -> None:
        embed = discord.Embed(
            color=color,
            description=msg
        )
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        return await ctx.send(embed=embed)

    async def send_error_msg(self, ctx: Union[commands.Context, discord.User], msg: str) -> None:
        return await self.send_titled_msg(ctx, 'Error', msg, 0xaa0000)

    async def send_success_msg(self, ctx: Union[commands.Context, discord.User], msg: str) -> None:
        return await self.send_titled_msg(ctx, 'Success', msg, 0x00aa00)

    async def send_usage_msg(self, ctx: Union[commands.Context, discord.User], msg: str) -> None:
        return await self.send_titled_msg(ctx, 'Usage', msg, 0x0000aa)

    async def send_info_msg(self, ctx: Union[commands.Context, discord.User], msg: str, *, thumbnail: str = None) -> None:
        return await self.send_untitled_msg(ctx, msg, 0x0000aa, thumbnail)

    async def send_titled_info_msg(self, ctx: Union[commands.Context, discord.User], title: str, msg: str) -> None:
        return await self.send_titled_msg(ctx, title, msg, 0x0000aa)

    async def on_ready(self) -> None:
        """
        Called when the client is done preparing the data received from Discord.
        Usually after login is successful.
        """

        print('\n------ startup complete ------')
        print(f'discord.py version: {discord.__version__}')
        print(f"logged in as: '{self.user.name}', id: {self.user.id}")
        print('member of these servers:')
        for guild in self.guilds:
            print(f"    name: '{guild.name}', id: {guild.id}")
        print(flush=True)
