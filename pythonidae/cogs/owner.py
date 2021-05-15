# coding=utf-8


# third-party modules - discord and related
#import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class OwnerCog(commands.Cog, name='owner'):

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    @print_context
    async def load_cog(self, ctx: commands.Context, cog: str) -> None:
        """
        Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.load_extension(cog)
        except commands.ExtensionAlreadyLoaded as e:
            msg = f'{cog} already loaded, attempting to reload...'
            await self.bot.send_info_msg(ctx, msg)
            await self.reload_cog(ctx, cog)
        except (
                commands.ExtensionNotFound,
                commands.NoEntryPointError,
                commands.ExtensionFailed,
        ) as e:
            msg = f'{type(e).__name__} - {e}'
            await self.bot.send_error_msg(ctx, msg)
        else:
            msg = f'Loaded: {cog}'
            await self.bot.send_success_msg(ctx, msg)

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
            msg = f'{type(e).__name__} - {e}'
            await self.bot.send_error_msg(ctx, msg)
        else:
            msg = f'Unloaded: {cog}'
            await self.bot.send_success_msg(ctx, msg)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    @print_context
    async def reload_cog(self, ctx: commands.Context, cog: str) -> None:
        """
        Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except commands.ExtensionNotLoaded as e:
            msg = f'{cog} not loaded, attempting to load...'
            await self.bot.send_info_msg(ctx, msg)
            await self.load_cog(ctx, cog)
        except (
                commands.ExtensionNotFound,
                commands.ExtensionAlreadyLoaded,
                commands.NoEntryPointError,
                commands.ExtensionFailed,
        ) as e:
            msg = f'{type(e).__name__} - {e}'
            await self.bot.send_error_msg(ctx, msg)
        else:
            msg = f'Reloaded: {cog}'
            await self.bot.send_success_msg(ctx, msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(OwnerCog(bot))
