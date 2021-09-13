# -*- coding: utf-8 -*-


# standard library modules
import copy
import json
import pathlib
import sys
import traceback
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa_help import KaaHelp
from kaantext import Kaantext


class Kaa(commands.Bot):
    """
    discord.ext.commands.Bot subclass
    """

    def __init__(self) -> None:
        """initializer"""

        intents = discord.Intents.all()
        commands.Bot.__init__(
            self,
            command_prefix=Kaa.prefixes_for,
            case_insensitive=True,
            help_command=KaaHelp(),
            intents=intents,
        )

        # formatting variables, should store these elsewhere
        self.indent = 4
        self.underline = True

        self.settings = self.load_settings()
        self.user_timezones = None
        self.load_extensions()
        self._owner = None

        # assorted
        self.blackjack_players = {}
        self.message_counts = {}

    async def get_context(self, message, *, cls=Kaantext):
        """
        overridden to use custom kaantext
        """

        return await super().get_context(message, cls=cls)

    # test this to make sure it's using the cache
    @staticmethod
    async def prefixes_for(bot, message: discord.Message, guild_prefixes={}) -> Union[str, list]:
        """
        A callable Prefix for our bot. This could be edited to allow per server prefixes.
        """

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
        """
        load the default extensions specified by the settings file
        """

        print()
        title = 'loading extensions'
        print(title)
        if self.underline:
            print(f"{'-' * len(title)}")

        for extension in self.settings['default_extensions']:
            try:
                self.load_extension(extension)
                print(f"{' ' * self.indent}{extension}")
            except (
                    commands.ExtensionNotFound,
                    commands.ExtensionAlreadyLoaded,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed
            ):
                print(f"Failed to load extension '{extension}'", file=sys.stderr)
                traceback.print_exc()

    async def get_owner(self) -> discord.User:
        """
        returns owner discord.User object, caches it for reuse
        """

        if not self._owner:
            app_info = await self.application_info()
            self._owner = app_info.owner
        return self._owner

    async def get_guild_settings(
            self,
            obj: Union[str, discord.Member, discord.Guild]
    ) -> Optional[dict]:
        """
        returns dict of guild specific settings
        """

        guild_id = None
        if isinstance(obj, str):
            for guild_settings in self.settings['guilds'].values():
                if guild_settings['nick'] == obj:
                    return copy.deepcopy(guild_settings)
            return None
        elif isinstance(obj, discord.Member):
            guild_id = obj.guild.id
        elif isinstance(obj, discord.Guild):
            guild_id = obj.id
        else:
            raise TypeError('obj must be a guild nickname str, a discord.Member instance, or a discord.Guild instance')
        if not guild_id:
            return None
        for guild_settings in self.settings['guilds'].values():
            if guild_settings['id'] == guild_id:
                return copy.deepcopy(guild_settings)
        return None

    async def on_ready(self) -> None:
        """
        Called when the client is done preparing the data received from Discord.
        Usually after login is successful.
        """

        print('\n--- startup complete ---\n')

        # print information about the bot
        bot_info = [
            ['bot username', f"'{self.user.name}#{self.user.discriminator}'"],
            ['bot id', self.user.id],
            ['server count', len(self.guilds)],
            ['discord.py version', discord.__version__],
        ]
        title = 'bot information'
        print(title)
        if self.underline:
            print(f"{'-' * len(title)}")

        # find the length of the longest title in bot_info for padding purposes (+1 for colon)
        sz = max((len(name) for name, _ in bot_info), default=0) + 1

        # iterate through info and print the titles and values
        for name, value in bot_info:
            print(f"{' ' * self.indent}{name + ':':<{sz}} {value}")
        print()

        # print information about the servers the bot is a member of
        title = 'current server names and ids'
        print(title)
        if self.underline:
            print(f"{'-' * len(title)}")

        # find the length of the longest Guild.name in self.guilds for padding purposes (+3 for colon and quotes)
        sz = max((len(guild.name) for guild in self.guilds), default=0) + 3

        # iterate through info and print the titles and values
        for guild in self.guilds:
            print(f"{' ' * self.indent}{guild.name.__repr__() + ':':<{sz}} {guild.id}")

        # print newline and flush the buffer to make sure everything is printed in a timely fashion
        print(flush=True)
