# coding=utf-8


# standard library modules
from datetime import datetime
import pytz

# third-party modules - discord and related
#import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class TimesCog(commands.Cog, name='times'):
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.timezones = {
            'deepak': 'Asia/Kolkata',

            'soren': 'Australia/Queensland',

            'romania': 'Europe/Bucharest',

            'maldives': 'Indian/Maldives',
            'yas': 'Indian/Maldives',
            'sam': 'Indian/Maldives',

            'turkey': 'Turkey',
            'system': 'Turkey',

            'tx': 'US/Central',
            'jaque': 'US/Central',
            'edobi': 'US/Central',
            'cowboy': 'US/Central',
            'sean': 'US/Central',

            'charlie': 'US/Eastern',
            'fats': 'US/Eastern',
            'mike': 'US/Eastern',
            'fl': 'US/Eastern',
            'nh': 'US/Eastern',
            'tony': 'US/Eastern',

            'or': 'US/Pacific',
            'jim': 'US/Pacific',
            'sir': 'US/Pacific',
            'ca': 'US/Pacific',
        }

    @commands.command()
    @commands.guild_only()
    @print_context
    async def time(
            self,
            ctx: commands.Context,
            timezone: str
    ) -> None:
        """show time for a time zone or person"""

        if timezone in self.timezones:
            timezone = self.timezones[timezone]
        elif timezone.lower() in self.timezones:
            timezone = self.timezones[timezone.lower()]

        time_zone = pytz.timezone(timezone)
        time_now_tz = datetime.now(time_zone)
        formatted_datetime = time_now_tz.strftime('%B %d %Y at %I:%M:%S %p')
        if timezone == 'Indian/Maldives':
            timezone = 'Maldives'
        await self.bot.send_titled_info_msg(ctx, timezone, formatted_datetime)


def setup(bot: PythonBot) -> None:
    bot.add_cog(TimesCog(bot))
