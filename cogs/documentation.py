# coding=utf-8


import io
from contextlib import redirect_stdout

# import discord
from discord.ext import commands


class DocumentationCog(commands.Cog, name="Documentation Commands"):
    """DocumentationCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='builtin')  # aliases=['alias1', 'alias2']
    async def show_builtin(self, ctx, cmd: str = None):
        """display python's help() for a built in function"""

        builtins = sorted(k for k, v in vars(__builtins__).items() if k.islower() and k.isalpha() and getattr(v, '__module__', '') == 'builtins')
        usage = '```\n' + 'Usage: `!builtin COMMAND`\n\n    Currently available commands:\n\n' + ' '.join(builtins) + '```'
        if not cmd:
            response = usage
        if cmd in builtins:
            f = io.StringIO()
            with redirect_stdout(f):
                help(cmd)
            output_string = f.getvalue()
            output_list = output_string.split('\n')
            output_string = '\n'.join(output_list[0:min(30, len(output_list))])
            response = f'```{output_string}```'
        else:
            response = usage
        await ctx.send(response)


def setup(bot):
    bot.add_cog(DocumentationCog(bot))
