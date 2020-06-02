# coding=utf-8


import discord
from discord.ext import commands

from utils import print_context


class MembersCog(commands.Cog, name='Member Commands'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @print_context
    async def joined(
            self,
            ctx: commands.Context,
            *,
            member: discord.Member
    ) -> None:
        """Says when a member joined."""

        await ctx.send(f'**`{member.display_name} joined at {member.joined_at}`**')

    @joined.error
    async def joined_handler(
            self,
            ctx: commands.Context,
            error: discord.DiscordException
    ) -> None:
        """display when a member joined the server"""

        if isinstance(error, commands.BadArgument):
            arg = ctx.message.clean_content.split()[-1]
            matches = [x for x in ctx.guild.members if x.display_name.lower() == arg.lower()]
            if not matches:
                msg = f'**`{error}`**'
            elif len(matches) == 1:
                msg = '**`this command is case-sensitive`**'
            else:
                msg = '**`multiple matches found, but your case is wrong for all of them`**'
            await ctx.send(msg)

    @commands.command(hidden=True)
    @print_context
    async def discobot(self, ctx: commands.Context, *args: str) -> None:
        """insult discobot"""

        if not args:
            await ctx.send('I am smarter than DiscoBot')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def test(self, ctx: commands.Context) -> None:
        """just a test command"""

        # for member in ctx.guild.members:
        #     print(f'{member.name}: {member.id}')
        await ctx.send('**`testing...`**')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(MembersCog(bot))
