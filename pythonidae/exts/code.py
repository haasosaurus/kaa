# -*- coding: utf-8 -*-


# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class CodeCog(commands.Cog, name='code'):
    """helper commands for sending code"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(aliases=['codeblock', 'code_block', 'code',])
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

    @commands.command(aliases=['md'])
    async def markdown(self, ctx: commands.Context):
        msg = '''\
**__CODEBLOCK SYNTAX HIGHLIGHTING__**
\`\`\`py
def func(n):
    for i in range(n):
        print(i)
\`\`\`
```py
def func(n):
    for i in range(n):
        print(i)
```
**__SPOILERS__**
\|\|spoiler\|\|
||spoiler||

**__MORE INFO__**
:link: Discord Markdown Text 101 <https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline->'''

        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(CodeCog(bot))
