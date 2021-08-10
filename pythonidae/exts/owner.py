# -*- coding: utf-8 -*-


# standard library modules
import sys
#from typing import Any, Mapping, Optional, Sequence, Tuple, Union

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Owner(commands.Cog, name='owner'):
    """cog with commands for the bot's owner"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.servers = None

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def shutdown(self, ctx: commands.Context) -> None:
        """Shuts down the bot and hopefully exits entirely"""

        msg = 'Shutting down, goodbye...'
        print(msg)
        await self.bot.send_info_msg(ctx, msg)
        await ctx.bot.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def flush(self, ctx: commands.Context) -> None:
        """flushes the buffers"""

        sys.stdout.flush()
        sys.stderr.flush()
        msg = 'Flushed stdout and stderr'
        await self.bot.send_success_msg(ctx, msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def say(
            self,
            ctx: commands.Context,
            target: str,
            channel_name: str,
            *words: str
    ) -> None:
        """makes pythonbot speak on target server"""

        if not words:
            msg = '!say SERVER CHANNEL *WORDS'
            await self.bot.send_usage_msg(ctx, msg)
            return

        guild_settings = await self.bot.get_guild_settings(target)
        if not guild_settings:
            msg = 'Target settings not found'
            await self.bot.send_error_msg(ctx, msg)
            return

        guild = discord.utils.get(self.bot.guilds, id=guild_settings['id'])
        if not guild:
            msg = 'Target not found'
            await self.bot.send_error_msg(ctx, msg)
            return

        channel = discord.utils.get(guild.text_channels, name=channel_name.lower())
        if not channel:
            msg = 'Channel not found'
            await self.bot.send_error_msg(ctx, msg)
            return

        msg = ' '.join('I' if word == 'i' else word for word in words)
        await channel.send(msg)

    @commands.group(case_insensitive=True, hidden=True)
    @commands.is_owner()
    @print_context
    async def status(self, ctx: commands.Context) -> None:
        """group for status setting commands"""

        pass

    @status.command(hidden=True, aliases=['listen', 'l'])
    @commands.is_owner()
    @print_context
    async def listening(self, ctx: commands.Context, *text) -> None:
        """sets status in listening ActivityType"""

        status = ' '.join(text)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        msg = f'Listening to {status}'
        await self.bot.send_titled_msg(ctx, 'Set status to:', msg, 0x00aa00)

    @status.command(hidden=True, aliases=['play', 'p'])
    @commands.is_owner()
    @print_context
    async def playing(self, ctx: commands.Context, *text) -> None:
        """sets status in playing ActivityType"""

        status = ' '.join(text)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
        msg = f'Playing {status}'
        await self.bot.send_titled_msg(ctx, 'Set status to:', msg, 0x00aa00)

    @commands.command(aliases=['rt'])
    @commands.is_owner()
    @print_context
    async def reload_test_ext(self, ctx: commands.Context):
        await ctx.invoke(self.bot.get_command('reload'), 'test')

    @commands.command(aliases=['rg'])
    @commands.is_owner()
    @print_context
    async def reload_games_ext(self, ctx: commands.Context):
        await ctx.invoke(self.bot.get_command('reload'), 'games')

    @commands.command(aliases=['re'])
    @commands.is_owner()
    @print_context
    async def reload_games_utils_embeds(self, ctx: commands.Context):
        await ctx.invoke(self.bot.get_command('reload'), 'games.utils.embeds')

    @commands.command(aliases=['rp'])
    @commands.is_owner()
    @print_context
    async def reload_profanity(self, ctx: commands.Context):
        await ctx.invoke(self.bot.get_command('reload'), 'profanity')


def setup(bot: PythonBot) -> None:
    bot.add_cog(Owner(bot))
