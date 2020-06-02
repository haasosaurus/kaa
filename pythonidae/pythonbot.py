#!/usr/bin/env python
# coding=utf-8


import json
import pathlib
import sys
import traceback

import discord
from discord.ext import commands


class PythonBot(commands.Bot):
    """commands.Bot sublass, trying to clean things up around here"""

    def __init__(self):
        commands.Bot.__init__(self, command_prefix=self.prefixes_for, case_insensitive=True)
        self.settings = self.load_settings()
        self.load_extensions()

    # test this to make sure it's using the cache
    @staticmethod
    async def prefixes_for(bot, message: discord.Message, guild_prefixes={}) -> str:
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

    async def on_ready(self) -> None:
        """
        Called when the client is done preparing the data received from Discord.
        Usually after login is successful and the Client.guilds and co. are
        filled up.
        """

        print(f'discord.py version: {discord.__version__}')
        print(f"logged in as: '{self.user.name}', id: {self.user.id}")
        print('member of these servers:')
        for guild in self.guilds:
            print(f"    name: '{guild.name}', id: {guild.id}")
