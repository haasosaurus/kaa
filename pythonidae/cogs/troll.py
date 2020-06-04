# coding=utf-8


# import discord
from discord.ext import commands

from utils import print_context


class TrollCog(commands.Cog, name='Troll Commands'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        help='shame people for their laziness',
        aliases=['lmgtfy'],
    )
    @print_context
    async def google(self, ctx: commands.Context, *keywords: str) -> None:
        """
        generate LMGTFY links when people try to make you their google bot
        """

        if not keywords:
            msg = '**`USAGE: !google OBVIOUS SEARCH KEYWORDS`**'
        else:
            msg = ':link: <https://lmgtfy.com/?q=' + '+'.join(keywords) + '>'
        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(TrollCog(bot))
