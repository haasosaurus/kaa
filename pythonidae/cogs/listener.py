# coding=utf-8


import discord
from discord.ext import commands

from utils import load_server_dict


class ListenerCog(commands.Cog, name='Listener'):
    """this cog listens for events"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.servers = None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """welcomes new members"""

        if not self.servers:
            self.servers = await load_server_dict()
        if not self.servers:
            print('ERROR: server dict is empty after loading', flush=True)
            return
        print('SUCCESS: loaded server dict', flush=True)

        server = member.guild
        if not server:
            print('ERROR: server not found for member', flush=True)
            return

        enabled = ['test', 'main', 'rust']
        servers = {self.servers[x] for x in enabled if x in self.servers}
        if server.id in servers:
            await server.system_channel.send(f'welcome {member.name}')

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """says goodbye to members after they've left, pointlessly"""

        if not self.servers:
            self.servers = await load_server_dict()
        if not self.servers:
            print('ERROR: server dict is empty after loading', flush=True)
            return
        print('SUCCESS: loaded server dict', flush=True)

        server = member.guild
        if not server:
            print('ERROR: server not found for member', flush=True)
            return

        enabled = ['test', 'main', 'rust']
        servers = {self.servers[x] for x in enabled if x in self.servers}
        if server.id in servers:
            await server.system_channel.send(f'goodbye forever {member.name}')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ListenerCog(bot))
