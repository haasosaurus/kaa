# coding=utf-8


import asyncio

# import discord
from discord.ext import commands

from utils import print_context


class CountdownCog(commands.Cog, name="Countdown Commands"):
    """pointless cog, move this to members"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(help='start a countdown timer')
    @commands.is_owner()
    @print_context
    async def countdown(self, ctx: commands.Context, *args) -> None:
        """countdown is a work in progress"""

        for i in range(5, -1, -1):
            await asyncio.sleep(1)
            await ctx.send(i)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CountdownCog(bot))
