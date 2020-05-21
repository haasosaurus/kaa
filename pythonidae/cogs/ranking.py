# coding=utf-8


import asyncio

import discord
from discord.ext import commands

from utils import print_context


class RankingCog(commands.Cog, name='Ranking Commands'):
    """pointless cog, move this to members"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot
        self.points = {}
        for guild in bot.guilds:
            if guild.id not in self.points:
                    self.points.update({guild.id:{}})
            for member in guild.members:
                if member not in self.points[guild.id]:
                    self.points[guild.id].update({member.id: 0})

    @commands.command()
    @commands.is_owner()
    @print_context
    async def give_points(
            self,
            ctx: commands.Context,
            member: discord.Member,
            points: int,
            reason: str = 'no reason'
    ) -> None:
        """blah"""

        if not member:
            await ctx.send('member not found')
            return

        if -100 <= points <= 100:
            gid = ctx.guild.id
            if member.id not in self.points[gid]:
                self.points[gid].update({member.id: 0})
            if ctx.author.id == member.id:
                await ctx.send("You can't high-five yourself!")
                return
            self.points[gid][member.id] += points
            await ctx.send(f'{points} points were given to {member} for {reason}!')

        else:
            await ctx.send('points not in valid range -100 <= points <= 100')

    @commands.command()
    @print_context
    async def show_points(
            self,
            ctx: commands.Context,
            member: discord.Member,
    ) -> None:
        """blah"""

        await ctx.send(f'{str(member)}: {self.points[ctx.guild.id][member.id]}')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RankingCog(bot))
