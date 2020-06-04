# coding=utf-8


import functools
from typing import Callable

from discord.ext import commands


def print_context(func: Callable) -> Callable:
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, commands.context.Context):
                print(
                    f"{arg.author}: '{arg.message.clean_content}' - "
                    f'author id: {arg.author.id}, '
                    f"guild: '{arg.guild.name if arg.guild else 'None'}', "
                    f"channel: '{arg.channel.name if arg.guild and arg.channel else 'None'}'",
                    flush=True
                )
                break
        return await func(*args, **kwargs)
    return inner
