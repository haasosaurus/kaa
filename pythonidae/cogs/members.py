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

        await ctx.send(f'**`{member.display_name} joined on {member.joined_at}`**')

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
                msg = 'member not found'
            elif len(matches) == 1:
                msg = 'this command is case-sensitive'
                idiots = ['SeeTheSaenz#5583', 'Marshall#8362', 'sansoo#6454']
                msg += ', idiot...' if str(ctx.author) in idiots else '...'
            else:
                msg = 'multiple matches found, but your case is wrong for all of them...'
            await ctx.send(msg)

    @commands.command(aliases=['PythonBot'])
    @print_context
    async def pythonbot(self, ctx: commands.Context, *args: str) -> None:
        """insult discobot"""

        if not args:
            await ctx.send('I am smarter than DiscoBot')

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def test(self, ctx: commands.Context) -> None:
        """just a test command"""

        await ctx.send('**`testing...`**')


    #---------- temporarily here so owner cog can be reloaded if this doesn't work ----------#
    # disabled for the time being

    # @commands.command(hidden=True)
    # @commands.is_owner()
    # @print_context
    # async def help_owner(self, ctx: commands.Context) -> None:
    #     """display help for all commands, even hidden ones"""

    #     pages = self.bot.formatter.format_help_for(ctx, self.bot)
    #     await ctx.send(pages)
    #     # await ctx.send('not implemented')
    #----------------------------------------------------------------------------------------#


def setup(bot: commands.Bot) -> None:
    bot.add_cog(MembersCog(bot))
