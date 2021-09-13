# -*- coding: utf-8 -*-


# standard library modules
import datetime
import itertools
import json
import pathlib
from typing import Union

# third-party packages
import pytz

# third-party packages - discord related
import discord
from discord.ext import commands
from reactionmenu import ButtonsMenu, ComponentsButton

# local modules
from kaa import Kaa
from utils import print_context
from better_menu import BetterMenu


class Times(commands.Cog, name='times'):
    """
    commands for setting and checking guild member's local time
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot
        self.timezone_rows = 18
        self.zero_w_space = '​'
        self.embed_color = 0xfed142

        user_timezones_path_str = 'resources/data/user_timezones.json'
        self.user_timezones_path = pathlib.Path(user_timezones_path_str).resolve()
        self.load_user_timezones()

        self.deprecated_path_str = 'resources/data/tz_deprecated.csv'
        self.timezones_deprecated = None
        self.aliases_path_str = 'resources/data/tz_aliases.csv'
        self.timezone_aliases = None
        self.timezone_to_country_code = None
        self.init_helper_dicts()

        self.timezones_by_offset = None
        self.offsets = None
        self.init_timezones()

    @staticmethod
    def keys_to_int(x):
        return {int(k): v for k, v in x}

    def init_helper_dicts(self):
        """
        """

        deprecated_path = pathlib.Path(self.deprecated_path_str).resolve()
        self.timezones_deprecated = {}
        with deprecated_path.open('r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    k, v = line.split(',')
                    self.timezones_deprecated.update({k: v})

        aliases_path = pathlib.Path(self.aliases_path_str).resolve()
        self.timezone_aliases = {}
        with aliases_path.open('r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    k, v = line.split(',')
                    self.timezone_aliases.update({k: v})

        self.timezone_to_country_code = {}
        for country_code, timezones in pytz.country_timezones.items():
            for timezone in timezones:
                self.timezone_to_country_code[timezone] = country_code.upper()

    def init_timezones(self):
        """
        """

        common_timezones = set(pytz.common_timezones)

        for deprecated, replacement in self.timezones_deprecated.items():
            if deprecated in common_timezones and replacement in common_timezones:
                common_timezones.remove(deprecated)

        for alias, canonical in self.timezone_aliases.items():
            if alias in common_timezones and canonical in common_timezones:
                common_timezones.remove(alias)

        common_timezones = sorted(common_timezones)

        utc_tz = pytz.timezone('UTC')
        utc_dt = datetime.datetime.now().astimezone(utc_tz)
        self.timezones_by_offset = {}
        for cur_tz_str in common_timezones:
            cur_tz = pytz.timezone(cur_tz_str)
            cur_dt = utc_dt.astimezone(cur_tz)
            utc_offset = cur_dt.strftime('%z').strip()

            # continue iterating if failed to create offset
            if not utc_offset:
                continue

            if utc_offset in self.timezones_by_offset:
                self.timezones_by_offset[utc_offset].append(cur_tz_str)
            else:
                self.timezones_by_offset.update({utc_offset: [cur_tz_str]})
        self.offsets = sorted(self.timezones_by_offset, key=int)

    @commands.command(
        name='timezone',
        aliases=['tz'],
        description='set your timezone',
        help='set your timezone',
    )
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)  # commands.BucketType.default is global
    @print_context
    async def timezone_command(
            self,
            ctx: commands.Context,
            timezone: str = None,
    ) -> None:
        """
        set your timezone
        """

        if timezone is not None:
            timezone = timezone.strip()
            if timezone not in pytz.all_timezones_set:
                msg = f"'{timezone}' is not a valid timezone"
                return self.bot.send_error_msg(ctx, msg)
            else:
                return await self.set_user_timezone(ctx, timezone)

        # create menu and buttons
        menu = BetterMenu(
            ctx,
            menu_type=ButtonsMenu.TypeEmbed,
            show_page_director=True,
            timeout=30,
            disable_buttons_on_timeout=True,
        )
        back_button = ComponentsButton(
            style=ComponentsButton.style.secondary,
            label='Back',
            custom_id=ComponentsButton.ID_PREVIOUS_PAGE
        )
        next_button = ComponentsButton(
            style=ComponentsButton.style.secondary,
            label='Next',
            custom_id=ComponentsButton.ID_NEXT_PAGE
        )
        select_button = ComponentsButton(
            style=ComponentsButton.style.green,
            label='Select',
            custom_id=ComponentsButton.ID_CALLER
        )
        exit_button = ComponentsButton(
            style=ComponentsButton.style.red,
            label='Exit',
            custom_id=ComponentsButton.ID_END_SESSION
        )

        # button handler callback
        updated = False
        selected_offset = None
        async def print_index():
            nonlocal updated
            nonlocal selected_offset
            if not updated:
                selected_offset = self.offsets[menu._pc.index]
                pages = await self.timezone_embeds(selected_offset)
                await menu.update(new_pages=pages, new_buttons=None)
                updated = True
            else:
                timezone_index = menu._pc.index
                timezone = self.timezones_by_offset[selected_offset][timezone_index]
                await self.set_user_timezone(ctx, timezone)
                await menu.stop(disable_buttons=True)
        menu.set_caller_details(print_index)

        # add buttons and pages
        menu.add_button(back_button)
        menu.add_button(next_button)
        menu.add_button(select_button)
        menu.add_button(exit_button)
        for offset in self.offsets:
            menu.add_page(await self.offset_embed(offset))
        utc_page = 0
        for i, x in enumerate(self.offsets):
            if x == '+0000':
                utc_page = i
                break

        await menu.start(utc_page)

    @timezone_command.error
    async def timezone_command_handler(
            self,
            ctx: commands.Context,
            error: commands.CommandError,
    ):
        """
        timezone command error handler
        """

        if isinstance(error, commands.MaxConcurrencyReached):
            msg = f"max concurrency reached for '{ctx.command}'."
            await self.bot.send_error_msg(ctx, msg)

    async def set_user_timezone(
            self,
            ctx: commands.Context,
            timezone: str
    ) -> None:
        """
        """

        self.bot.user_timezones[ctx.author.id] = timezone
        await self.save_user_timezones()
        msg = f"Set your timezone to '{timezone}'"
        await self.bot.send_info_msg(ctx, msg, color=self.embed_color)

    async def save_user_timezones(self) -> None:
        """
        """

        with self.user_timezones_path.open('w') as f:
            json.dump(self.bot.user_timezones, f, indent=4)

    def load_user_timezones(self) -> None:
        """
        """

        with self.user_timezones_path.open('r') as f:
            self.bot.user_timezones = json.load(f, object_pairs_hook=Times.keys_to_int)

    async def timezone_embeds(self, offset: str):
        """
        """

        embeds = []
        for timezone in self.timezones_by_offset[offset]:
            embed = discord.Embed(
                title=f'UTC {offset:>5}',
                description='choose a timezone',
                color=self.embed_color
            )
            embed.add_field(name='timezone', value=timezone)
            embeds.append(embed)
        return embeds

    async def offset_embed(self, offset: str) -> discord.Embed:
        """
        """

        timezone_names = self.timezones_by_offset[offset]

        # initialize embed
        embed = discord.Embed(
            title=f'UTC{offset}',
            description='choose a utc offset group',
            color=self.embed_color
        )

        # initialize position and add first column
        i = self.timezone_rows
        col = itertools.islice(itertools.chain(timezone_names, itertools.repeat(self.zero_w_space)), i)
        col = '\n'.join(col)
        embed.add_field(name='timezones', value=col, inline=True)

        # add as many more columns as required
        while i < len(timezone_names):
            col = itertools.islice(timezone_names, i, i + self.timezone_rows)
            col = '\n'.join(col)
            embed.add_field(name=self.zero_w_space, value=col, inline=True)
            i += self.timezone_rows

        return embed

    @commands.command(
        name='time',
        aliases=[],
        description='show time for timezone or user',
        help='show time for timezone or user',
    )
    # @commands.guild_only()
    @print_context
    async def time(
            self,
            ctx: commands.Context,
            user_or_timezone: Union[discord.Member, discord.User, str],
    ) -> None:
        """
        show time for timezone or user
        """

        # attempt to get valid timezone
        timezone_str = None
        if isinstance(user_or_timezone, str):
            if user_or_timezone not in pytz.all_timezones_set:
                return await self.bot.send_error_msg(ctx, f"'{user_or_timezone}' is not a valid timezone")
            else:
                timezone_str = user_or_timezone
        else:
            if user_or_timezone.id not in self.bot.user_timezones:
                return await self.bot.send_error_msg(ctx, "user's timezone not saved")
            timezone_str = self.bot.user_timezones[user_or_timezone.id]

        # setup flag
        country_code = self.timezone_to_country_code.get(timezone_str)
        if country_code:
            flag_url = f'https://www.countryflags.io/{country_code}/shiny/64.png'
        else:
            flag_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Pirate_Flag_of_Jack_Rackham.svg/320px-Pirate_Flag_of_Jack_Rackham.svg.png'

        # create timezone aware datetime
        timezone = pytz.timezone(timezone_str)
        dt_now = datetime.datetime.now(timezone)
        if timezone_str == 'Indian/Maldives':
            timezone_str = 'Maldives'
        formatted_dt = dt_now.strftime('%B %d %Y at %I:%M:%S %p')

        # initialize user_name
        user_name = None
        utc_offset = dt_now.strftime('%z')
        if not isinstance(user_or_timezone, str):
            user_name = user_or_timezone.display_name

        # create embed
        embed = discord.Embed(
            color=0xfed142,
        )
        embed.add_field(name='Time', value=formatted_dt, inline=False)
        embed.add_field(name='Timezone', value=timezone_str, inline=False)
        embed.add_field(name='UTC offset', value=utc_offset, inline=False)
        if user_name:
            embed.set_author(name=user_name, icon_url=user_or_timezone.avatar_url)
        embed.set_footer(text=self.zero_w_space, icon_url=flag_url)

        await ctx.send(embed=embed)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Times(bot))
