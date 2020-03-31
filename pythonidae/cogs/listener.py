# coding=utf-8


# import discord
from discord.ext import commands

from utils import load_server_dict


class ListenerCog(commands.Cog, name='Listener'):

    def __init__(self, bot):
        self.bot = bot
        self.servers = None

    async def member_join(self, member):
        if not self.servers:
            self.servers = await load_server_dict()
        if not self.servers:
            print('ERROR: server dict is empty after loading', flush=True)
        else:
            print('SUCCESS: loaded server dict', flush=True)
            server = member.guild
            enabled_servers = {self.servers[name] for name in ['test', 'main'] if name in self.servers}
            if server and server.id in enabled_servers:
                await server.system_channel.send(f'welcome {member.name}')

    async def member_remove(self, member):
        if not self.servers:
            self.servers = await load_server_dict()
        if not self.servers:
            print('ERROR: server dict is empty after loading', flush=True)
        else:
            print('SUCCESS: loaded server dict', flush=True)
            server = member.guild
            enabled_servers = {self.servers[name] for name in ['test', 'main'] if name in self.servers}
            if server and server.id in enabled_servers:
                await server.system_channel.send(f'goodbye {member.name}')


def setup(bot):
    listener = ListenerCog(bot)
    bot.add_listener(listener.member_join, 'on_member_join')
    bot.add_listener(listener.member_remove, 'on_member_remove')
    bot.add_cog(listener)
