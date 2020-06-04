# coding=utf-8


import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import print_context


class OwnerCog(commands.Cog, name='owner'):

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

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
    async def flush(self, ctx: commands.Context) -> None:
        """flushes the buffers"""

        sys.stdout.flush()
        sys.stderr.flush()
        await ctx.send('**`SUCCESS - flushed stdout and stderr`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def say(
            self,
            ctx: commands.Context,
            target: str = None,
            channel: str = None,
            *words: str
    ) -> None:
        """makes pythonbot speak on target server"""

        if not words:
            await ctx.send('**`Usage: !say SERVER CHANNEL *WORDS`**')
            return

        guild_settings = await self.bot.get_guild_settings(target)
        if not guild_settings:
            await ctx.send('**`ERROR: target settings not found`**')
            return

        guild = discord.utils.get(self.bot.guilds, id=guild_settings['id'])
        if not guild:
            await ctx.send('**`ERROR: target not found`**')
            return

        channel = discord.utils.get(guild.text_channels, name=channel.lower())
        if not channel:
            await ctx.send('**`ERROR: channel not found`**')
            return

        msg = ' '.join('I' if word == 'i' else word for word in words)
        await channel.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(OwnerCog(bot))
