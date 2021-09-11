# -*- coding: utf-8 -*-


# standard library modules
from typing import Union

# third-party packages - discord related
import discord
from discord.ext import commands
import dislash
from dislash import slash_commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Members(commands.Cog, name='members'):
    """assorted commands for guild members"""

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
    ) -> None:
        """Says when a member joined."""

        if member is None:
            member = ctx.message.author

        if member == ctx.message.author:
            title = 'You joined:'
        else:
            title = f"{member.display_name} joined:"

        formatted_datetime = member.joined_at.strftime('%B %d %Y at %I:%M:%S %p')
        await self.bot.send_titled_info_msg(ctx, title, formatted_datetime)

    @joined.error
    async def joined_handler(
            self,
            ctx: commands.Context,
            error: commands.CommandError,
    ) -> None:
        """error handling for joined command"""

        if isinstance(error, commands.BadArgument):
            msg = str(error)
            await self.bot.send_error_msg(ctx, msg)

    @commands.command(name='avatar')
    @print_context
    async def avatar_command(self, ctx: commands.Context, user: Union[discord.Member, discord.User] = None) -> None:
        if user is None:
            user = ctx.author
        url = user.avatar_url
        await ctx.send(url)

    @slash_commands.slash_command(
        name='avatar',
        description="sends a user's avatar",
        guild_ids=[
            791589784626921473,  # ck
            864816273618763797,  # kaa
        ],
        options=[
            dislash.Option(
                name='user',
                description='another user, or omitted for yourself',
                type=dislash.OptionType.USER,
                required=False,
            ),
        ]
    )
    async def avatar_slash(self, inter: dislash.MessageInteraction, user: Union[discord.Member, discord.User] = None) -> None:
        if user is None:
            user = inter.author
        url = user.avatar_url
        await inter.reply(url)

    @commands.command(
        help='shame tony for his laziness',
        aliases=['search', 'lmgtfy', 'lmgt',],
    )
    @commands.guild_only()
    @print_context
    async def google(
            self,
            ctx: commands.Context,
            *obvious_keywords: str
    ) -> None:
        """
        generate letmegooglethat links for help vampires/askholes
        """

        if not obvious_keywords:
            msg = '!google OBVIOUS SEARCH KEYWORDS'
            await self.bot.send_usage_msg(ctx, msg)
        else:
            keywords = '+'.join(obvious_keywords)
            msg = ':link: http://letmegooglethat.com/?q=' + keywords
            await self.bot.send_info_msg(ctx, msg)

    @commands.command(hidden=True)
    @commands.guild_only()
    @print_context
    async def hello(self, ctx: commands.Context) -> None:
        """A simple command which only responds to the owner of the bot."""

        if ctx.author.id == self.bot.owner_id:
            msg = 'Hello father'
        else:
            msg = f'Hello {ctx.author.display_name}'
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Members(bot))
