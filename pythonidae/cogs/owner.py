# coding=utf-8


import json
import os
import pathlib
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import print_context

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.servers = None

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    @print_context
    async def load_cog(self, ctx: commands.Context, *, cog: str) -> None:
        """
        Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.load_extension(cog)
        except (
                commands.ExtensionNotFound,
                commands.ExtensionAlreadyLoaded,
                commands.NoEntryPointError,
                commands.ExtensionFailed,
        ) as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - loaded cog`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    @print_context
    async def unload_cog(self, ctx: commands.Context, *, cog: str) -> None:
        """
        Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionNotLoaded as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - unloaded cog`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    @print_context
    async def reload_cog(self, ctx: commands.Context, *, cog: str) -> None:
        """
        Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except (
                commands.ExtensionNotLoaded,
                commands.ExtensionNotFound,
                commands.ExtensionAlreadyLoaded,
                commands.NoEntryPointError,
                commands.ExtensionFailed,
        ) as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - reloaded cog`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def shutdown(self, ctx: commands.Context) -> None:
        """Shuts down the bot and hopefully exits entirely"""

        await ctx.send('**`Shutting down...`**')
        print('Shutting down...')
        await ctx.bot.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def hello(self, ctx: commands.Context) -> None:
        """A simple command which only responds to the owner of the bot."""

        await ctx.send('Hello father')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def flush(self, ctx: commands.Context) -> None:
        """flushes the buffers"""

        sys.stdout.flush()
        sys.stderr.flush()
        await ctx.send('**`SUCCESS - flushed stdout and stderr`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def reload_env(self, ctx: commands.Context) -> None:
        """reload .env file"""

        load_dotenv()
        await ctx.send('**`SUCCESS - reloaded env`**')

    @commands.command(aliases=['reload_server_dict'], hidden=True)
    @commands.is_owner()
    @print_context
    async def load_server_dict(self, ctx: commands.Context) -> None:
        """load/reload the json server configuration file"""

        path = pathlib.Path(os.getenv('DISCORD_SERVERS_JSON')).resolve()
        with path.open('r') as servers_file:
            self.servers = json.load(servers_file)
        await ctx.send('**`SUCCESS - loaded server dict`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def help_owner(self, ctx: commands.Context) -> None:
        """display help for all commands, even hidden ones"""

        await ctx.send('not implemented')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def say(
            self,
            ctx: commands.Context,
            target: str = None,
            *words: str
    ) -> None:
        """makes pythonbot speak on target server"""

        if not words:
            await ctx.send('**`Usage: !say SERVER *WORDS`**')
            return

        if not self.servers:
            await self.load_server_dict(ctx)
        if target not in self.servers:
            await ctx.send('**`ERROR: Unknown target server`**')
            return

        for i, word in enumerate(words):
            if word == 'i':
                words[i] = 'I'

        target_server = discord.utils.get(
            self.bot.guilds,
            id=self.servers[target]
        )
        if not target_server:
            msg = "**`ERROR: discord.utils.get did not get target_server`**"
            await ctx.send(msg)
            return

        msg = ' '.join(words)
        await target_server.system_channel.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(OwnerCog(bot))
