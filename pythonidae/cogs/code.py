# coding=utf-8


import discord
from discord.ext import commands

from pythonbot import PythonBot
from utils import print_context


class CodeCog(commands.Cog, name='code'):
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @print_context
    async def block(
            self,
            ctx: commands.Context,
            lang: str,
            message: discord.Message,
    ) -> None:
        """resend someone's message as a codeblock"""

        if message.clean_content.startswith('```'):
            await self.bot.send_error_msg(ctx, "I think that's already a code block dude")
            return

        msg = f'```{lang}\n{message.clean_content}\n```'
        await ctx.send(msg)

    @block.error
    async def block_handler(self, ctx, error):
        """block error handler"""

        if isinstance(error, commands.MissingPermissions):
            error_msg = 'missing administrator permissions'
            await self.bot.send_error_msg(ctx, error_msg)
        else:
            raise error


def setup(bot: PythonBot) -> None:
    bot.add_cog(CodeCog(bot))
