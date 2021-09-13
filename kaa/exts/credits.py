# -*- coding: utf-8 -*-


# standard library modules
import pathlib
import sqlite3

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Credits(commands.Cog, name='credits'):
    """credits cog"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.blacklist = set()
        self.db_path = pathlib.Path('./points_db.sqlite3').resolve()


    @commands.Cog.listener(name='on_message')
    async def message_credits(self, message: discord.Message) -> None:
        """credit assignment message listener"""

        pass


    @commands.command(
        name='blacklist',
        aliases=[],
        description='blacklist user credits functionality',
        help='blacklist user credits functionality',
        hidden=True,
    )
    @commands.guild_only()
    @commands.is_owner()
    @print_context
    async def blacklist_command(
            self,
            ctx: commands.Context,
            member: discord.Member
    ) -> None:
        """blacklist a member from using the points system"""

        self.blacklist.add(member.id)
        await ctx.send(f'**`member "{member.display_name}" has been blacklisted`**')

    async def db_connect(self):
        con = sqlite3.connect(self.db_path)
        return con


    @commands.command(
        name='credits_give',
        aliases=[],
        description='give a member points',
        help='give a member points',
        cooldown_after_parsing=True,
    )
    @commands.guild_only()
    @commands.cooldown(1, 90, commands.BucketType.user)
    @print_context
    async def credits_give_command(
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


    @credits_give_command.error
    async def credits_give_command_handler(
            self,
            ctx: commands.Context,
            error: discord.DiscordException
    ) -> None:
        """error handler for points_give"""

        if isinstance(error, commands.BadArgument):
            await ctx.send(f'**`{error}`**')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"**`you can't do that for {round(error.retry_after)} seconds`**")


    @commands.command(
        name='credits_info',
        aliases=[],
        description='display user credit information',
        help='display user credit information',
        ignore_extra=True,

    )
    @commands.guild_only()
    @print_context
    async def credits_info_command(
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


    @credits_info_command.error
    async def credits_info_command_handler(
            self,
            ctx: commands.Context,
            error: discord.DiscordException
    ) -> None:
        """error handler for points_show"""

        if isinstance(error, commands.BadArgument):
            await ctx.send(f'**`{error}`**')


def setup(bot: PythonBot) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Credits(bot))
