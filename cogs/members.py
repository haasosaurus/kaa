# coding=utf-8


import discord
from discord.ext import commands


class MembersCog(commands.Cog, name="Member Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""

        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='pythonbot', aliases=['PythonBot'])
    async def cool_bot(self, ctx):
        """insult discobot"""

        await ctx.send('I am smarter than DiscoBot')


def setup(bot):
    bot.add_cog(MembersCog(bot))
