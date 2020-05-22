# coding=utf-8


import asyncio
import pathlib
import sqlite3

import discord
from discord.ext import commands

from utils import print_context


class RankingCog(commands.Cog, name='Ranking Commands'):
    """ranking cog"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot
        db_path = pathlib.Path('./points_db.sqlite3').expanduser().resolve()


        self.points = {}
        for guild in bot.guilds:
            if guild.id not in self.points:
                    self.points.update({guild.id:{}})
            for member in guild.members:
                if member not in self.points[guild.id]:
                    self.points[guild.id].update({member.id: 0})


    # async def db_connect(self):
    #     conn = sqlite3.connect(self.db_path)
    #     return conn


    @commands.command()
    # @commands.is_owner()
    @print_context
    async def give_points(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
            points: int = None,
            reason: str = 'no reason'
    ) -> None:
        """give points to a member"""

        if not member:
            await ctx.send('**`member not specified or not found`**')
            return

        if not points:
            await ctx.send('**`points not specified or points was 0`**')
            return

        if not -100 <= points <= 100:
            await ctx.send('**`points not in valid range -100 <= points <= 100`**')
            return

        if ctx.author.id == member.id:
            await ctx.send("**`You can't high-five yourself!`**")
            return


        gid = ctx.guild.id
        # con = await self.db_connect()
        # with con:
        #     cur = con.cursor()
        #     s = f'CREATE TABLE IF NOT EXISTS {gid} ...;'
        #     cur.execute('SELECT from ')




        if member.id not in self.points[gid]:
            self.points[gid].update({member.id: 0})
        self.points[gid][member.id] += points
        await ctx.send(f'**`{points} points were given to {member} for {reason}!`**')

    @commands.command()
    @print_context
    async def show_points(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
    ) -> None:
        """display a member's points"""

        # doesn't work
        if not member:
            await ctx.send('**`member not found`**')
            return

        await ctx.send(f"**`{str(member)}'s points: {self.points[ctx.guild.id][member.id]}`**")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RankingCog(bot))
