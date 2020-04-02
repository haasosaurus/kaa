# coding=utf-8


import asyncio
import functools
import json
import os
import pathlib
from typing import Callable

from discord.ext import commands


def print_context(func: Callable) -> Callable:
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, commands.context.Context):
                print(
                    str(arg.author) + ': ' + str(arg.message.clean_content),
                    flush=True
                )
                break
        return await func(*args, **kwargs)
    return inner


async def load_server_dict() -> dict:
    servers_path = pathlib.Path(os.getenv('DISCORD_SERVERS_JSON')).resolve()
    with servers_path.open('r') as servers_file:
        servers = json.load(servers_file)
        return servers
