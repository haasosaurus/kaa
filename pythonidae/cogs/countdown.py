# coding=utf-8


import asyncio

# import discord
from discord.ext import commands


class CountdownCog(commands.Cog, name="Countdown Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='start a countdown timer')
    @commands.is_owner()
    async def countdown(self, ctx, *args):
        for i in range(5, -1, -1):
            await asyncio.sleep(1)
            await ctx.send(i)


def setup(bot):
    bot.add_cog(CountdownCog(bot))
