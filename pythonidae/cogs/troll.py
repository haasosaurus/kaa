# coding=utf-8


# third-party modules - discord and related
#import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class TrollCog(commands.Cog, name='troll'):
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        help='shame tony for his laziness',
        aliases=['search', 'lmgtfy', 'lmgt',],
    )
    @print_context
    async def google(self, ctx: commands.Context, *obvious_keywords: str) -> None:
        """
        generate letmegooglethat links for help vampires
        """

        if not obvious_keywords:
            msg = '!google OBVIOUS SEARCH KEYWORDS'
            await self.bot.send_usage_msg(ctx, msg)
        else:
            keywords = '+'.join(obvious_keywords)
            msg = ':link: http://letmegooglethat.com/?q=' + keywords
            await self.bot.send_info_msg(ctx, msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(TrollCog(bot))
