# coding=utf-8


import json
import os
import pathlib
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv


class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot
        self.servers = None

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """
        Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.load_extension(cog)
        except Exception as e:  # pylint: disable=broad-except
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - loaded cog`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):  # pylint: disable=arguments-differ
        """
        Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.unload_extension(cog)
        except Exception as e:  # pylint: disable=broad-except
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - unloaded cog`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """
        Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner
        """

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:  # pylint: disable=broad-except
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS - reloaded cog`**')

    @commands.command(name='shutdown', hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot and hopefully exits entirely"""

        await ctx.send('**`Shutting down...`**')
        print('Shutting down...')
        await ctx.bot.logout()

    @commands.command(name='hello', hidden=True)
    @commands.is_owner()
    async def only_me(self, ctx):
        """A simple command which only responds to the owner of the bot."""

        await ctx.send('Hello father')

    @commands.command(name='flush', hidden=True)
    @commands.is_owner()
    async def flush_buffer(self, ctx):
        sys.stdout.flush()
        sys.stderr.flush()
        await ctx.send('**`SUCCESS - flushed stdout and stderr`**')

    @commands.command(name='reload_env', hidden=True)
    @commands.is_owner()
    async def reload_env(self, ctx):
        load_dotenv()
        await ctx.send('**`SUCCESS - reloaded env`**')

    @commands.command(
        name='reload_servers',
        aliases=['refresh_server_dict', 'reload_server_dict', 'refresh_servers'],
        hidden=True,
    )
    @commands.is_owner()
    async def load_server_dict(self, ctx):
        servers_path = pathlib.Path(os.getenv('DISCORD_SERVERS_JSON')).expanduser().resolve()
        with servers_path.open('r') as servers_file:
            self.servers = json.load(servers_file)
        await ctx.send('**`SUCCESS - loaded server dict`**')

    @commands.command(name='say', hidden=True)
    @commands.is_owner()
    async def say(self, ctx, *args):
        if args:
            target, *words = args
            if not words or not target:
                await ctx.send('**`Usage: !say SERVER *WORDS`**')
            else:
                if not self.servers:
                    await self.load_server_dict(ctx)
                if target not in self.servers:
                    await ctx.send('**`Error: Unknown target server`**')
                else:
                    for i, word in enumerate(words):
                        if word == 'i':
                            words[i] = 'I'
                    target_server = discord.utils.get(self.bot.guilds, id=self.servers[target])
                    if target_server:
                        await target_server.system_channel.send(' '.join(words))
                    else:
                        await ctx.send('**`Error: failed to initialize \'target_server\' with \'discord.utils.get\'`**')


def setup(bot):
    bot.add_cog(OwnerCog(bot))
