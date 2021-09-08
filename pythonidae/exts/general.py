# -*- coding: utf-8 -*-


# third-party packages - discord related
# import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class General(commands.Cog, name='general'):
    """assorted non-guild specific commands"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(aliases=['h'])
    @print_context
    async def help_(self, ctx: commands.Context):
        await ctx.send_help()


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(General(bot))
