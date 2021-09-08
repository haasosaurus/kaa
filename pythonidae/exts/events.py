# -*- coding: utf-8 -*-


# third-party modules
import dateparser
import pytz

# third-party packages - discord related
import discord
from discord.ext import commands, tasks

# local modules
from pythonbot import PythonBot
from utils import print_context


class Events(commands.Cog, name='events'):
    def __init__(self, bot: PythonBot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    @print_context
    async def taskgen(self, ctx: commands.Context, seconds: int) -> None:

        @tasks.loop(seconds=seconds, count=1)
        async def inner_task() -> None:
            pass

        @inner_task.before_loop
        async def before_inner_task() -> None:
            pass

        @inner_task.after_loop
        async def after_inner_task() -> None:
            await ctx.send('timer complete')

        inner_task.start()

    @commands.command()
    @commands.is_owner()
    @print_context
    async def local_time_test(self, ctx: commands.Context, *, future_datetime: str):
        """
        dateparse test
        """

        # stop if unable to load caller's timezone
        timezone = self.bot.user_timezones.get(ctx.author.id, None)
        if timezone is None:
            msg = "Your timezone isn't registered with the bot, set it with the timezone command"
            return await self.bot.send_error_msg(ctx, msg)

        # parse future_datetime str argument
        local_dt = dateparser.parse(
            future_datetime,
            languages=['en',],
            settings={
                'TIMEZONE': timezone,
                'RETURN_AS_TIMEZONE_AWARE': True,
                'PREFER_DATES_FROM': 'future',
            },
        )

        # debugging
        local_dt_formatted = local_dt.strftime('%B %d %Y at %I:%M:%S %p (UTC%z)')

        utc_timezone = pytz.timezone('UTC')
        utc_dt = local_dt.astimezone(utc_timezone)
        utc_dt_formatted = utc_dt.strftime('%B %d %Y at %I:%M:%S %p (UTC%z)')

        debug_msg_lines = [
            '```',
            f"local time\n{'-' * 10}",
            f'{local_dt}',
            f'{local_dt_formatted}',
            '',
            f"utc time\n{'-' * 8}",
            f'{utc_dt}',
            f'{utc_dt_formatted}',
            '```',
        ]
        debug_msg = '\n'.join(debug_msg_lines)

        embed = discord.Embed(
            title='local time test',
            description='check footer for input time in your local time',
            color=0xefa607,
            timestamp=utc_dt,
        )
        embed.set_footer(
            text='local time:',
            icon_url='https://cdn.iconscout.com/icon/premium/png-256-thumb/alarm-clock-2080486-1754199.png',
        )

        # send the message
        await ctx.send(debug_msg, embed=embed)


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Events(bot))
