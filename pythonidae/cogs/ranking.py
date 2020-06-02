# coding=utf-8


#---------------------------- ideas ----------------------------#
# limit giving points to once a minute
# put a time when last points given as a column
# implement ban and unban methods
# implement leaderboard method, call it points_top
# implement set_points method
# implement exception handling
#---------------------------------------------------------------#


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
        self.blacklist = set()
        self.db_path = pathlib.Path('./points_db.sqlite3').resolve()

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    @print_context
    async def points_blacklist(self, ctx: commands.Context, member: discord.Member) -> None:
        self.blacklist.add(member.id)
        await ctx.send('**`lol`**')

    async def db_connect(self):
        con = sqlite3.connect(self.db_path)
        return con

    @commands.command(aliases=['give_points', 'point_give', 'give_point'])
    @commands.guild_only()
    # @commands.is_owner()
    @commands.cooldown(1, 90, commands.BucketType.user)
    @print_context
    async def points_give(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
            points: int = None,
            *reason: str,
    ) -> None:
        """give a member points"""

        if ctx.author.id in self.blacklist:
            return
        if not member:
            await ctx.send('**`member not specified or not found`**')
            return
        if not points:
            await ctx.send('**`points not specified or points was 0`**')
            return
        if not -100 <= points <= 100 and ctx.author.id != self.bot.owner_id:
            await ctx.send('**`points not in valid range -100 <= points <= 100`**')
            return
        if ctx.author.id == member.id and ctx.author.id != self.bot.owner_id:
            await ctx.send("**`You can't high-five yourself!`**")
            return

        con = await self.db_connect()
        with con:
            cur = con.cursor()

            # create server table if needed
            create_server_table = f'''
                CREATE TABLE IF NOT EXISTS server_{ctx.guild.id} (
                member_id integer PRIMARY KEY,
                points integer NOT NULL DEFAULT 0
                )'''
            cur.execute(create_server_table)

            # create member row if needed
            cur.execute(
                f'INSERT OR IGNORE INTO server_{ctx.guild.id} (member_id) VALUES(?)',
                (member.id,)
            )

            # update points for member
            cur.execute(
                f'UPDATE server_{ctx.guild.id} SET points = points + ? WHERE member_id = ?',
                (points, member.id)
            )

            # get member's new point total
            cur.execute(
                f'SELECT * from server_{ctx.guild.id} where member_id = ?',
                (member.id, )
            )
            total_points = cur.fetchone()[1]

            # create remaining elements of and send result message
            if not reason:
                reason = 'no reason'
            else:
                reason = ' '.join(reason)
            await ctx.send(
                f'**`{points} points were given to {member.display_name} for {reason}! '
                f'They now have {total_points} points!`**'
            )

    @commands.command(aliases=['show_points', 'show_point', 'point_show'])
    @commands.guild_only()
    @print_context
    async def points_show(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
    ) -> None:
        """display a member's points"""

        con = await self.db_connect()
        with con:
            cur = con.cursor()

            # create server table if needed
            create_server_table = f'''
                CREATE TABLE IF NOT EXISTS server_{ctx.guild.id} (
                member_id integer PRIMARY KEY,
                points integer NOT NULL DEFAULT 0
                )'''
            cur.execute(create_server_table)

            # create member row if needed
            cur.execute(
                f'INSERT OR IGNORE INTO server_{ctx.guild.id} (member_id) VALUES(?)',
                (member.id,)
            )

            # get member's point total
            cur.execute(
                f'SELECT * from server_{ctx.guild.id} where member_id = ?',
                (member.id, )
            )
            total_points = cur.fetchone()[1]

            # send result message
            await ctx.send(f'**`{member.display_name} has {total_points} points`**')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RankingCog(bot))
