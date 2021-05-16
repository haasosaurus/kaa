# coding=utf-8


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
            member: discord.Member,
            count: int,
    ) -> None:
        """backend private method for handling rm command"""

        message_blacklist = set()

        # don't delete the message that called the command
        if ctx.message:
            message_blacklist.add(ctx.message)

        # limit the maximum messages able to be deleted
        message_limit = 50
        if count > message_limit:
            msg = f'max messages that can be deleted per usage is {message_limit}, limiting count...'
            sent_msg = await self.bot.send_info_msg(ctx, msg)
            if sent_msg:
                message_blacklist.add(sent_msg)
            count = message_limit

        # deleted messages until i reaches count
        i = 0
        async for message in ctx.channel.history(limit=1_000):
            if message.author == member:

                # skip messages in the blacklist
                if message in message_blacklist:
                    continue

                await message.delete()
                i += 1
                if i >= count:
                    break

        # send amount of messages actually deleted
        msg = f'deleted {i} messages'
        await self.bot.send_info_msg(ctx, msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(AdminCog(bot))
