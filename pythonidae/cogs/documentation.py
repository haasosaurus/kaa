# coding=utf-8


import builtins
import inspect
from contextlib import redirect_stdout

# import discord
from discord.ext import commands


class DocumentationCog(commands.Cog, name="Documentation Commands"):
    """DocumentationCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='docs', aliases=['builtin'])
    async def show_docs(self, ctx, cmd: str = None, mthd: str = None):
        """display documentation for a built in function or type"""

        usage = (
            '**```\n' + 'Usage: `!docs COMMAND`\n\nCurrently available commands:\n\n' +
            '  '.join(sorted(builtins.__dict__.keys(), key=lambda x: x.lower())) + '```**'
        )
        if not cmd:
            response = usage
        elif cmd in vars(builtins):
            target = vars(builtins)[cmd]
            if mthd:
                if mthd in vars(target):
                    target = vars(target)[mthd]
                else:
                    target = None
                    response = '**`ERROR: method not found`**'
            if target:
                method_list = [method for method in dir(target) if not method.startswith('__')]
                if method_list:
                    methods = '\n\nMethods:\n    ' + '  '.join(method_list) + '\n'
                else:
                    methods = ''
                response = '**```'
                try:
                    response_body = cmd + str(inspect.signature(target)) + '\n    ' + target.__doc__
                    response += response_body
                    if methods:
                        response += methods
                except (ValueError, TypeError):
                    response_body = inspect.getdoc(target)
                    if response_body:
                        response += response_body
                        if methods:
                            response += methods
                    else:
                        response += '**`docs not found, sorry...`**'
                response += '```**'
        else:
            response = usage
        await ctx.send(response)


def setup(bot):
    bot.add_cog(DocumentationCog(bot))
