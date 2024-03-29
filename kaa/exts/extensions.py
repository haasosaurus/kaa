# -*- coding: utf-8 -*-


# standard library modules
import sys
import traceback

# third-party packages - discord related
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context


class Extensions(commands.Cog, name='extensions'):
    """cog with commands for extension management"""

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        name='load',
        aliases=[],
        description='load extensions',
        help='load extensions',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def load_extensions(
            self,
            ctx: Kaantext,
            *extensions: str,
    ) -> None:
        """
        load extensions
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.load_extension(extension)
            except commands.ExtensionAlreadyLoaded as e:
                await self.reload_extensions(ctx, extension)
            except (
                    commands.ExtensionNotFound,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed,
            ) as e:
                traceback.print_exception(
                    type(e),
                    e,
                    e.__traceback__,
                    file=sys.stderr,
                )
                msg = f'{type(e).__name__} - {e}'
                await ctx.send_error_msg(msg)
            else:
                msg = f'Loaded: {extension}'
                await ctx.send_success_msg(msg)

    @commands.command(
        name='unload',
        aliases=[],
        description='unload extensions',
        help='unload extensions',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def unload_extensions(
            self,
            ctx: Kaantext,
            *extensions: str,
    ) -> None:
        """
        unload extensions
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.unload_extension(extension)
            except commands.ExtensionNotLoaded as e:
                traceback.print_exception(
                    type(e),
                    e,
                    e.__traceback__,
                    file=sys.stderr,
                )
                msg = f'{type(e).__name__} - {e}'
                await ctx.send_error_msg(msg)
            else:
                msg = f'Unloaded: {extension}'
                await ctx.send_success_msg(msg)

    @commands.command(
        name='reload',
        aliases=[],
        description='reload extensions',
        help='reload extensions',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_extensions(
            self,
            ctx: Kaantext,
            *extensions: str,
    ) -> None:
        """
        reload extensions
        """

        for extension in extensions:
            if not extension.startswith('exts.'):
                extension = 'exts.' + extension

            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except commands.ExtensionNotLoaded as e:
                await self.load_extensions(ctx, extension)
            except (
                    commands.ExtensionNotFound,
                    commands.ExtensionAlreadyLoaded,
                    commands.NoEntryPointError,
                    commands.ExtensionFailed,
            ) as e:
                traceback.print_exception(
                    type(e),
                    e,
                    e.__traceback__,
                    file=sys.stderr,
                )
                msg = f'{type(e).__name__} - {e}'
                await ctx.send_error_msg(msg)
            else:
                msg = f'Reloaded: {extension}'
                await ctx.send_success_msg(msg)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Extensions(bot))
