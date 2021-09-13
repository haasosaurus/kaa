# -*- coding: utf-8 -*-


# third-party packages - discord related
# import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context


class General(commands.Cog, name='general'):
    """assorted non-guild specific commands"""

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        name='help_',
        aliases=[],
        description='old new help command test',
        help='old new help command test',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def help_command(self, ctx: Kaantext):
        """
        old new help command test
        """

        await ctx.send_help()


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(General(bot))
