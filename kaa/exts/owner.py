# -*- coding: utf-8 -*-


# standard library modules
import sys
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Owner(commands.Cog, name='owner'):
    """general bot owner commands"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        name='poweroff',
        aliases=['shutdown'],
        description='shuts down the bot',
        help='shuts down the bot and hopefully exits gracefully and entirely',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def shutdown_command(self, ctx: commands.Context) -> None:
        """
        shuts down the bot and hopefully exits gracefully and entirely
        """

        msg = 'Shutting down, goodbye...'
        print(msg)
        await self.bot.send_info_msg(ctx, msg)
        await ctx.bot.close()

    @commands.command(
        name='flush',
        aliases=[],
        description='flushes stdout and stderr',
        help='flushes stdout and stderr buffers',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def flush_command(self, ctx: commands.Context) -> None:
        """
        flushes stdout and stderr buffers
        """

        sys.stdout.flush()
        sys.stderr.flush()
        msg = 'Flushed stdout and stderr'
        await self.bot.send_success_msg(ctx, msg)

    @commands.command(
        name='say',
        aliases=[],
        description='speak through kaa',
        help='make kaa say whatever you want',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def say_command(
            self,
            ctx: commands.Context,
            target: str,
            channel_name: str,
            *words: str,
    ) -> None:
        """
        make kaa say whatever you want
        """

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

    @commands.group(
        name='status',
        description='set listening/playing status',
        help='set listening/playing status',
        hidden=True,
        case_insensitive=True,
    )
    @commands.is_owner()
    @print_context
    async def status_command_group(self, ctx: commands.Context) -> None:
        """
        group for status setting commands
        """

        pass

    @status_command_group.command(
        name='listening',
        aliases=[],
        description='set listening status',
        help='set listening status ActivityType',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def listening_command(
            self,
            ctx: commands.Context,
            *text: str,
    ) -> None:
        """
        set listening status ActivityType
        """

        status = ' '.join(text)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        msg = f'Listening to {status}'
        await self.bot.send_titled_msg(ctx, 'Set status to:', msg, 0x00aa00)

    @status_command_group.command(
        name='playing',
        aliases=[],
        description='set playing status',
        help='set playing status ActivityType',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def playing_command(self, ctx: commands.Context, *text) -> None:
        """
        set playing status ActivityType
        """

        status = ' '.join(text)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
        msg = f'Playing {status}'
        await self.bot.send_titled_msg(ctx, 'Set status to:', msg, 0x00aa00)

    @commands.command(
        name='rt',
        aliases=[],
        description='`reload test` alias',
        help='alias for command `reload test`',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_test_command(self, ctx: commands.Context):
        """
        alias for command `reload test`
        """

        await ctx.invoke(self.bot.get_command('reload'), 'test')

    @commands.command(
        name='rg',
        aliases=[],
        description='`reload games` alias',
        help='alias for command `reload games`',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_games_command(self, ctx: commands.Context):
        """
        alias for command `reload games`
        """

        await ctx.invoke(self.bot.get_command('reload'), 'games')

    @commands.command(
        name='re',
        aliases=[],
        description='`reload game.utils.embeds` alias',
        help='alias for command `reload game.utils.embeds`',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_games_utils_embeds_command(self, ctx: commands.Context):
        """
        alias for command `reload game.utils.embeds`
        """

        await ctx.invoke(self.bot.get_command('reload'), 'games.utils.embeds')

    @commands.command(
        name='rp',
        aliases=[],
        description='`reload profanity` alias',
        help='alias for command `reload profanity`',
        hidden=True,
    )
    @commands.is_owner()
    @print_context
    async def reload_profanity_command(self, ctx: commands.Context):
        """
        alias for command `reload profanity`
        """

        await ctx.invoke(self.bot.get_command('reload'), 'profanity')


def setup(bot: PythonBot) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Owner(bot))
