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
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        # self.message_counts = {}

    @commands.command(
        aliases=['rm'],
        hidden=True
    )
    @commands.is_owner()
    @commands.guild_only()
    @print_context
    async def delete(
            self,
            ctx: commands.Context,
            member: discord.Member,
            count: int = 1
    ) -> None:
        """delete messages from a member"""

        cnt = 0
        async for msg in ctx.channel.history(limit=1_000):
            if msg.author == member:
                print(f'{msg.clean_content.__repr__()}')
                await msg.delete()
                cnt += 1
                if cnt == count:
                    break

    @commands.command(
        aliases=[],
        hidden=True,
    )
    @commands.is_owner()
    @commands.guild_only()
    @print_context
    async def prune_by_reaction(
            self,
            ctx: commands.Context,
            message: discord.Message,
            *white_list_roles: str,
    ) -> None:
        """prune members by their lack of a reaction"""

        guild = ctx.guild
        roles = set()
        for x in white_list_roles:
            role = discord.utils.get(guild.roles, name=x)
            if not role:
                self.bot.send_error_msg(f"role '{role}' not found, aborting...")
                return
            roles.add(role)

        white_list = []
        non_white_list = []
        reacted = set()
        kick_list = []
        new_members_list = []
        cur_time = datetime.datetime.now()

        for reaction in message.reactions:
            async for member in reaction.users():
                reacted.add(member)

        async for member in guild.fetch_members(limit=1_000):
            if any(role in roles for role in member.roles):
                white_list.append(member)
            else:
                non_white_list.append(member)

        for member in non_white_list:
            joined = member.joined_at
            if not joined or (member not in reacted and (cur_time - member.joined_at).days <= 14):
                new_members_list.append(member)

            elif member not in reacted:
                kick_list.append(member)

        white_list_str = (
            '```\n' +
            'white list\n' +
            '----------\n' +
            ', '.join(sorted(member.display_name for member in white_list)) +
            '\n```'
        )
        new_members_list_str = (
            '```\n' +
            'new members list\n' +
            '----------------\n' +
            ', '.join(sorted(member.display_name for member in new_members_list)) +
            '\n```'
        )
        reacted_str = (
            '```\n' +
            'reacted list\n' +
            '------------\n' +
            ', '.join(sorted(member.display_name for member in reacted)) +
            '\n```'
        )
        kick_list_str = (
            '```\n' +
            'kick list\n' +
            '---------\n' +
            ', '.join(sorted(member.display_name for member in kick_list)) +
            '\n```'
        )

        await ctx.send(white_list_str)
        await ctx.send(new_members_list_str)
        await ctx.send(reacted_str)
        await ctx.send(kick_list_str)

    @commands.command(
        aliases=[],
        hidden=True,
    )
    @commands.is_owner()
    @commands.guild_only()
    @print_context
    async def update_counts(self, ctx: commands.Context) -> None:
        """make dict of members message counts"""

        guild = ctx.guild
        self.bot.message_counts[guild] = {}

        async for member in ctx.guild.fetch_members(limit=None):
            self.bot.message_counts[guild][member] = {}

        for channel in ctx.guild.channels:
            if not isinstance(channel, discord.TextChannel):
                continue

            async for message in channel.history(limit=None):
                if message.author not in self.bot.message_counts[guild]:
                    continue

                if channel in self.bot.message_counts[guild][message.author]:
                    self.bot.message_counts[guild][message.author][channel] += 1
                else:
                    self.bot.message_counts[guild][message.author][channel] = 1

    @commands.command(
        aliases=[],
        hidden=True,
    )
    @commands.has_role('admin')
    @commands.guild_only()
    @print_context
    async def message_count(self, ctx: commands.Context, member: discord.Member) -> None:
        """get message count for a member"""

        total_count = 0
        member_dict = self.bot.message_counts[ctx.guild][member]
        channel_sz = max(map(lambda x: len(x.name), member_dict)) + 5
        count_sz = max(map(lambda x: len(str(x)), member_dict.values()))

        msg_list = []

        for channel, count in member_dict.items():
            total_count += count
            s = f"{channel.name + ':':<{channel_sz}} {count:>{count_sz}}"
            msg_list.append(s)
        total_str = f'total: {total_count}'
        msg_list.append('-' * len(total_str))
        msg_list.append(total_str)
        msg = '```\n' + '\n'.join(msg_list) + '\n```'
        await ctx.send(msg)

    @commands.command(
        aliases=[],
        hidden=True,
    )
    @commands.is_owner()
    @commands.guild_only()
    @print_context
    async def test(self, ctx: commands.Context) -> None:
        """just a test command"""

        msg = 'testing...'
        await self.bot.send_info_msg(ctx, msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(AdminCog(bot))
