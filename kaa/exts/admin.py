# -*- coding: utf-8 -*-


# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context


class Admin(commands.Cog, name='admin'):
    """commands for server admins"""

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        name='rm_messages',
        aliases=['rm'],
        description='delete messages from a member',
        help='delete messages from a member',
        hidden=True,
        cooldown_after_parsing=True,
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @print_context
    async def rm_messages_command(
            self,
            ctx: Kaantext,
            member: discord.Member,
            count: int = 1,
    ) -> None:
        """delete messages from a member"""

        return await self._rm(ctx, member, count)

    @rm_messages_command.error
    async def rm_messages_command_handler(
            self,
            ctx: Kaantext,
            error: commands.CommandError,
    ) -> None:
        """error handler for rm"""

        # if command is on cooldown for the user that called it
        if isinstance(error, commands.CommandOnCooldown):
            _, original_ctx, member, count = ctx.args

            # if the owner is on cooldown, allow the command anyways
            if original_ctx.author.id == self.bot.owner_id:
                await self._rm(ctx, member, count)

            # if the user who called the command isn't the owner
            else:
                msg = f"you can't do that for {round(error.retry_after)} seconds"
                await ctx.send_error_msg(msg)

        # if member or count conversion failed
        elif isinstance(error, commands.BadArgument):
            msg = f'{error}'
            await ctx.send_error_msg(msg)

        # member doesn't have permission
        elif isinstance(error, commands.MissingPermissions):
            msg = f"You don't have permission to run '{ctx.command}'."
            await ctx.send_error_msg(msg)

        # user tries to use command in a private message
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                msg = f"'{ctx.command}' can't be used in private messages."
                return await ctx.send_error_msg(msg)
            except:
                pass

        # this might be pointless
        else:
            raise error

    async def _rm(
            self,
            ctx: Kaantext,
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
            sent_msg = await ctx.send_info_msg(msg)
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
        await ctx.send_info_msg(msg)

    @commands.command(
        name='wipe_channel',
        aliases=[],
        description='remove all channel messages',
        help='deletes a text channel and then creates a identical empty channel to remove all messages easily',
        hidden=True,
    )
    @commands.has_permissions(administrator=True)
    # @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @print_context
    async def wipe_channel_command(
            self,
            ctx: Kaantext,
            channel: discord.TextChannel,
    ) -> None:
        """
        deletes and then creates a matching channel to remove all messages easily
        """

        # save old position
        position = channel.position

        # replace channel with clone
        clone = await channel.clone()
        await channel.delete()

        # move clone to old position
        await clone.edit(position=position)

        # send success message
        msg = f'Wiped channel {clone.mention}'
        await ctx.send_success_msg(msg)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Admin(bot))
