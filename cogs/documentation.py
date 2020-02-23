# coding=utf-8


import io
from contextlib import redirect_stdout

# import discord
from discord.ext import commands


class DocumentationCog(commands.Cog, name="Documentation Commands"):
    """DocumentationCog"""


    builtins = (
        'abs', 'delattr', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 'setattr', 'any',
        'dir', 'hex', 'next', 'slice', 'ascii', 'divmod', 'id', 'object', 'sorted', 'bin', 'enumerate',
        'input', 'oct', 'staticmethod', 'bool', 'eval', 'int', 'open', 'str', 'breakpoint', 'exec',
        'isinstance', 'ord', 'sum', 'bytearray', 'filter', 'issubclass', 'pow', 'super', 'bytes',
        'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property', 'type', 'chr',
        'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip',
        'compile', 'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='builtin')  # aliases=['alias1', 'alias2']
    async def show_builtin(self, ctx, cmd: str = None):
        """display python's help() for a built in function"""

        usage = '```\n' + 'Usage: `!builtin COMMAND`\n\n    Currently available commands:\n\n' + ' '.join(self.builtins) + '```'
        if not cmd:
            response = usage
        elif cmd in self.builtins:
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
