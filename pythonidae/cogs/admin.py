# coding=utf-8


# standard library modules
import datetime
#import itertools
#import json
#import traceback

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class AdminCog(commands.Cog, name='admin'):
    """commands for server admins"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        #self.message_counts = {}

    @commands.command(
        aliases=['delete'],
        cooldown_after_parsing=True,
        hidden=True,
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @print_context
    async def rm(
            self,
            ctx: commands.Context,
            member: discord.Member,
            count: int = 1,
    ) -> None:
        """delete messages from a member"""

        return await self._rm(ctx, member, count)

    @rm.error
    async def rm_handler(
            self,
            ctx: commands.Context,
            error: commands.CommandError,
    ) -> None:
        """error handler for points_give"""

        # if member or count conversion failed
        if isinstance(error, commands.BadArgument):
            msg = f'{error}'
            await self.bot.send_error_msg(ctx, msg)

        # if command is on cooldown for the user that called it
        elif isinstance(error, commands.CommandOnCooldown):
            _, original_ctx, member, count = ctx.args

            # if the owner is on cooldown, allow the command anyways
            if original_ctx.author.id == self.bot.owner_id:
                await self._rm(ctx, member, count)

            # if the user who called the command isn't the owner
            else:
                msg = f"you can't do that for {round(error.retry_after)} seconds"
                await self.bot.send_error_msg(ctx, msg)

        # member doesn't have permission
        elif isinstance(error, commands.MissingPermissions):
            msg = f"You don't have permission to run '{ctx.command}'."
            await self.bot.send_error_msg(ctx, msg)

        # user tries to use command in a private message
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                msg = f"'{ctx.command}' can't be used in private messages."
                return await self.bot.send_error_msg(ctx, msg)
            except:
                pass

        # this might be pointless
        else:
            raise error

    async def _rm(
            self,
            ctx: commands.Context,
            member:discord.Member,
            count: int,
    ) -> None:
        """backend private method for handling rm command"""

        i = 0
        async for msg in ctx.channel.history(limit=100):
            if msg.author == member:

                # don't delete the message that called the command
                # if caller is deleting their own messages
                if ctx.author.id == member.id and i == 0:
                    i += 1
                    count += 1
                    continue

                # delete all others in this potentially new range
                print(f"deleting: '{msg.clean_content}'")
                await msg.delete()
                i += 1
                if i >= count:
                    break


def setup(bot: PythonBot) -> None:
    bot.add_cog(AdminCog(bot))
