# coding=utf-8


# standard library modules
#import itertools
#import traceback

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class MembersCog(commands.Cog, name='members'):
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @print_context
    async def joined(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
            # *,
    ) -> None:
        """Says when a member joined."""

        if member is None:
            member = ctx.message.author

        if member == ctx.message.author:
            header = 'You joined:'
        else:
            header = f"{member.display_name} joined:"

        formatted_datetime = member.joined_at.strftime('%B %d %Y at %I:%M:%S %p')
        await self.bot.send_titled_info_msg(ctx, header, formatted_datetime)

    @joined.error
    async def joined_handler(
            self,
            ctx: commands.Context,
            error: discord.DiscordException
    ) -> None:
        """error handling for joined command"""

        if isinstance(error, commands.BadArgument):
            msg = 'Member not found'
            await self.bot.send_error_msg(ctx, msg)

    @commands.command(hidden=True)
    @print_context
    async def hello(self, ctx: commands.Context) -> None:
        """A simple command which only responds to the owner of the bot."""

        if ctx.author.id == self.bot.owner_id:
            msg = 'Hello father'
        else:
            msg = f'Hello {ctx.author.display_name}'
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(MembersCog(bot))
