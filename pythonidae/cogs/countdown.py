# coding=utf-8


# standard library modules
import asyncio

# third-party modules - discord and related
#import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class CountdownCog(commands.Cog, name='Countdown Commands'):
    """pointless cog, move this to members"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.kill_countdown = False

    @commands.command()
    @commands.is_owner()
    @print_context
    async def kill_cd(self, ctx):
        self.kill_countdown = True
        await ctx.send('attempting to kill countdown...')

    @commands.command(help='Usage: !countdown MINUTES')
    @commands.is_owner()
    @print_context
    async def countdown(self, ctx: commands.Context, minutes: int, title: str, *args: str) -> None:
        """countdown is a work in progress"""

        if not minutes or not title:
            await ctx.send('Usage: !countdown MINUTES TITLE')
            return

        min_per_day = 1440
        if minutes > min_per_day:
            await ctx.send("sorry, i'm only gonna do countdowns that are one day or less for now")
        hours, minutes = divmod(minutes, 60)
        if hours:
            await ctx.send(f'{hours} {"hours" if hours > 1 else "hour"} and {minutes} minutes until {title}')
        else:
            await ctx.send(f'{minutes} minutes until {title}')

        while hours:
            if self.kill_countdown:
                await ctx.send('killing countdown')
                self.kill_countdown = False
                return
            if minutes:
                await asyncio.sleep(minutes * 60)
                minutes = 0
                await ctx.send(f'{hours} hours until {title}')
            elif hours == 1:
                await ctx.send(f'1 hour until {title}')
                hours = 0
                minutes = 30
                await asyncio.sleep(minutes * 60)
            else:
                await ctx.send(f'{hours} hours until {title}')
                hours -= 1
                await asyncio.sleep(60 * 60)

        while minutes:
            if self.kill_countdown:
                await ctx.send('killing countdown')
                self.kill_countdown = False
                return
            await asyncio.sleep(60)
            minutes -= 1
            await ctx.send(f'{minutes} minutes until {title}')

        await ctx.send(f'countdown over, time for {title}')


def setup(bot: PythonBot) -> None:
    bot.add_cog(CountdownCog(bot))
