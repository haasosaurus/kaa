# coding=utf-8


# import discord
from discord.ext import commands


class TrollCog(commands.Cog, name="Troll Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='shame people for their laziness')
    async def google(self, ctx, *args):
        response = ':link: <https://lmgtfy.com/?q='
        response += '+'.join(args)
        response += '>'
        await ctx.send(response)


def setup(bot):
    bot.add_cog(TrollCog(bot))
