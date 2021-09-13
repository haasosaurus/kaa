# -*- coding: utf-8 -*-


# standard library modules - typing
from typing import Mapping, Optional, List, Union

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from constants import Colors, Chars


class KaaHelp(commands.HelpCommand):

    def __init__(self, admin=False, owner=False, **options):
        super().__init__(**options)
        self.admin = admin
        self.owner = owner


    async def send_bot_help(
            self,
            mapping: Mapping[Optional[commands.Cog], List[commands.Command]],
    ) -> None:
        """
        sends primary bot help command
        """

        embed = discord.Embed(
            color=Colors.kaa,
        )
        # for setting max embed width
        title = f'Kaa{Chars.U00A0}Help{Chars.U3000 * 30}{Chars.U200B}'
        embed.set_author(name=title)

        for cog, cog_commands in mapping.items():
            if cog is None:
                name = f'other'
            else:
                name = f'{cog.qualified_name}'
            value = ''
            for command in cog_commands:
                if command.hidden and not self.owner:
                    continue
                if value:
                    value += '\n'
                description = ''
                if command.description:
                    description = f'(*{command.description}*)'
                value += f'**\u3000{command.name}** {description}'
            if not value:
                continue
            embed.add_field(name=name, value=value, inline=False)
        dest = self.get_destination()
        await dest.send(embed=embed)


    async def send_cog_help(self, cog: commands.Cog) -> None:
        # create breadcrumbs
        breadcrumbs = '`'
        breadcrumbs += f'{cog.qualified_name} > '
        breadcrumbs += ' > '.join(cog.qualified_name.split('.'))
        breadcrumbs += '`'
        breadcrumbs += Chars.BLANK_LINE
        breadcrumbs += str(cog)


        # initialize embed
        title = f'{cog.qualified_name}'
        embed = discord.Embed(
            color=Colors.kaa,
            title=title,
            description=breadcrumbs,
        )

        # expand embed to max width
        author = f'Kaa{Chars.SPACE}Help{Chars.EXPANDER}'
        embed.set_author(name=author)

        # name = f'{cog.qualified_name}'
        name = 'Commands'
        # name = title
        value = ''
        for command in cog.get_commands():

            # command_or_group: Union[commands.Command, commands.Group]
            # cog.walk_commands()

            if command.hidden and not self.owner:
                continue

            if value:
                value += '\n'
            description = ''
            if command.description:
                description = f'(*{command.description}*)'
            value += f'**\u3000{command.name}** {description}'

        embed.add_field(name=name, value=value, inline=False)
        dest = self.get_destination()
        await dest.send(embed=embed)


    async def send_group_help(self, group: commands.Group) -> None:
        if group.hidden and not self.owner:
            return

        # create breadcrumbs
        breadcrumbs = '`'
        if group.cog:
            breadcrumbs += f'{group.cog_name} > '
        breadcrumbs += ' > '.join(group.qualified_name.split())
        breadcrumbs += '`'

        # initialize embed
        title = f'{group.name}'
        embed = discord.Embed(
            color=Colors.kaa,
            title=title,
            description=breadcrumbs,
        )

        # expand embed to max width
        author = f'Kaa{Chars.SPACE}Help{Chars.EXPANDER}'
        embed.set_author(name=author)

        count = 0
        command: commands.Command
        for command in group.commands:
            if command.hidden and not self.owner:
                continue

            name = f'{command.name}'
            value = f'*{command.description}*\n`{self.get_command_signature(command)}`'
            embed.add_field(name=name, value=value, inline=False)
            count += 1

        if count:
            dest = self.get_destination()
            await dest.send(embed=embed)


    async def send_command_help(self, command: commands.Command) -> None:
        if command.hidden and not self.owner:
            return

        # create breadcrumbs
        breadcrumbs = '`'
        if command.cog:
            breadcrumbs += f'{command.cog_name} > '
        breadcrumbs += ' > '.join(command.qualified_name.split())
        breadcrumbs += '`'

        # initialize embed
        title = f'{command.name}'
        embed = discord.Embed(
            color=Colors.kaa,
            title=title,
            description=breadcrumbs,
        )

        # expand embed to max width
        author = f'Kaa{Chars.SPACE}Help{Chars.EXPANDER}'
        embed.set_author(name=author)

        name = f'{Chars.NEWLINE_LEFT}Command Information'
        value = f'{command.help}'
        embed.add_field(name=name, value=value, inline=False)

        name = f'{Chars.NEWLINE_LEFT}Usage'
        value = f'`{self.get_command_signature(command)}`'
        embed.add_field(name=name, value=value, inline=False)

        dest = self.get_destination()
        await dest.send(embed=embed)
