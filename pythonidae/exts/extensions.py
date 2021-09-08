# -*- coding: utf-8 -*-


# standard library modules
import sys
import traceback

# third-party packages - discord related
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Extensions(commands.Cog, name='extensions'):
    """cog with commands for extension management"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    @print_context
    async def load_extensions(self, ctx: commands.Context, *extensions: str) -> None:
        """
        command to load an extension
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.load_extension(extension)
            except commands.ExtensionAlreadyLoaded as e:
                msg = f'{extension} already loaded, attempting to reload...'
                await self.bot.send_info_msg(ctx, msg)
                await self.reload_extensions(ctx, extension)
            except (
                    commands.ExtensionNotFound,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed,
            ) as e:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                msg = f'{type(e).__name__} - {e}'
                await self.bot.send_error_msg(ctx, msg)
            else:
                msg = f'Loaded: {extension}'
                await self.bot.send_success_msg(ctx, msg)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    @print_context
    async def unload_extensions(self, ctx: commands.Context, *extensions: str) -> None:
        """
        command to unload an extension
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.unload_extension(extension)
            except commands.ExtensionNotLoaded as e:
                msg = f'{type(e).__name__} - {e}'
                await self.bot.send_error_msg(ctx, msg)
            else:
                msg = f'Unloaded: {extension}'
                await self.bot.send_success_msg(ctx, msg)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    @print_context
    async def reload_extensions(self, ctx: commands.Context, *extensions: str) -> None:
        """
        command to reload an extension
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except commands.ExtensionNotLoaded as e:
                msg = f'{extension} not loaded, attempting to load...'
                await self.bot.send_info_msg(ctx, msg)
                await self.load_extensions(ctx, extension)
            except (
                    commands.ExtensionNotFound,
                    commands.ExtensionAlreadyLoaded,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed,
            ) as e:
                msg = f'{type(e).__name__} - {e}'
                await self.bot.send_error_msg(ctx, msg)
            else:
                msg = f'Reloaded: {extension}'
                await self.bot.send_success_msg(ctx, msg)


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Extensions(bot))
