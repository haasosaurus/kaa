# -*- coding: utf-8 -*-


# standard library modules
import functools
import pathlib
from typing import Callable

# third-party packages - discord related
import discord
from discord.ext import commands


def print_context(func: Callable) -> Callable:
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, commands.Context):
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


def load_texts(text_paths: dict) -> None:
    """
    loads text data from text files
    """

    texts = {}
    for name, path in text_paths.items():
        with pathlib.Path(path).resolve().open('r') as f:
            texts[name] = f.read()
    return texts
