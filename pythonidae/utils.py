# coding=utf-8


import asyncio
import json
import os
import pathlib


async def load_server_dict() -> dict:
    servers_path = pathlib.Path(os.getenv('DISCORD_SERVERS_JSON')).expanduser().resolve()
    with servers_path.open('r') as servers_file:
        servers = json.load(servers_file)
        return servers
    return {}
