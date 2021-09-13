# -*- coding: utf-8 -*-


# standard library modules
from typing import Union

# third-party packages - discord related
import discord
from discord.ext import commands
import dislash
from dislash import slash_commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context


class Members(commands.Cog, name='members'):
    """general commands for server members"""

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        name='joined',
        aliases=[],
        description='shows member joined date and time',
        help='shows member joined date and time',
    )
    @commands.guild_only()
    @print_context
    async def joined_command(
            self,
            ctx: Kaantext,
            member: discord.Member = None,
    ) -> None:
        """
        sends member joined date and time
        """

        if member is None:
            member = ctx.message.author

        if member == ctx.message.author:
            title = 'You joined:'
        else:
            title = f"{member.display_name} joined:"

        formatted_datetime = member.joined_at.strftime('%B %d %Y at %I:%M:%S %p')
        await self.bot.send_titled_info_msg(ctx, title, formatted_datetime)

    @joined_command.error
    async def joined_command_handler(
            self,
            ctx: Kaantext,
            error: commands.CommandError,
    ) -> None:
        """error handling for joined command"""

        if isinstance(error, commands.BadArgument):
            msg = str(error)
            await ctx.send_error_msg(msg)

    @commands.command(
        name='avatar',
        aliases=[],
        description='sends user avatar url',
        help='sends user avatar url',
    )
    @print_context
    async def avatar_command(self, ctx: Kaantext, user: Union[discord.Member, discord.User] = None) -> None:
        """
        sends user avatar url
        """

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
                required=False,  # False is default
            ),
        ]
    )
    @slash_commands.guild_only()
    async def avatar_slash(self, inter: dislash.SlashInteraction, user: Union[discord.Member, discord.User] = None) -> None:
        if user is None:
            user = inter.author
        url = user.avatar_url
        await inter.reply(url)

    @commands.command(
        name='google',
        aliases=['search', 'lmgt', 'lmgtfy'],
        description='generate letmegooglethat links',
        help='generate letmegooglethat links for help vampires/askholes, shame tony for his laziness',
    )
    @commands.guild_only()
    @print_context
    async def google_command(
            self,
            ctx: Kaantext,
            *obvious_keywords: str,
    ) -> None:
        """
        generate letmegooglethat links for help vampires/askholes, shame tony for his laziness
        """

        if not obvious_keywords:
            msg = '!google OBVIOUS SEARCH KEYWORDS'
            await self.bot.send_usage_msg(ctx, msg)
        else:
            keywords = '+'.join(obvious_keywords)
            msg = ':link: http://letmegooglethat.com/?q=' + keywords
            await ctx.send_info_msg(msg)

    @commands.command(
        name='hello',
        aliases=[],
        description='says hello',
        help='says hello',
        hidden=True,
    )
    @commands.guild_only()
    @print_context
    async def hello_command(self, ctx: Kaantext) -> None:
        """A simple command which only responds to the owner of the bot."""

        if ctx.author.id == self.bot.owner_id:
            msg = 'Hello father'
        else:
            msg = f'Hello {ctx.author.display_name}'
        await ctx.send(msg)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Members(bot))
