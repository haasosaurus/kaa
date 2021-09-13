# -*- coding: utf-8 -*-


# standard library modules
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from constants import Colors, Chars


class Kaantext(commands.Context):
    async def send_titled_msg(
            self,
            title: str,
            msg: str,
            color: int,
    ) -> discord.Message:
        """
        sends a message embed to the given context - includes a title
        """

        embed = discord.Embed(
            color=color,
        )
        embed.add_field(
            name=title,
            value=msg,
            inline=False
        )
        return await self.send(embed=embed)

    async def send_untitled_msg(
            self,
            msg: str,
            color: int,
            thumbnail: str = None,
    ) -> discord.Message:
        """
        sends a message embed to the given context
        """

        embed = discord.Embed(
            color=color,
            description=msg
        )
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        return await self.send(embed=embed)

    async def send_error_msg(
            self,
            msg: str,
            *,
            color=Colors.error,
    ) -> discord.Message:
        """
        sends an error message embed to the given context
        """

        return await self.send_titled_msg('Error', msg, color)

    async def send_success_msg(
            self,
            msg: str,
            *,
            color=Colors.kaa,
    ) -> discord.Message:
        """
        sends a success message embed to the given context
        """

        return await self.send_titled_msg('Success', msg, color)

    async def send_usage_msg(
            self,
            msg: str,
            *,
            color=Colors.kaa,
    ) -> discord.Message:
        """
        sends a usage message embed to the given context
        """

        return await self.send_titled_msg('Usage', msg, color)

    async def send_info_msg(
            self,
            msg: str,
            *,
            thumbnail: str = None,
            color=Colors.kaa,
    ) -> discord.Message:
        """
        sends an info message embed to the given context
        """

        return await self.send_untitled_msg(msg, color, thumbnail)

    async def send_titled_info_msg(
            self,
            title: str,
            msg: str,
            *,
            color=Colors.kaa,
    ) -> discord.Message:
        """
        sends an info message embed to the given context - includes a title
        """

        return await self.send_titled_msg(title, msg, color)
