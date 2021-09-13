# -*- coding: utf-8 -*-


# standard library modules
import base64
import io
import sys
import traceback

# third-party packages - discord related
import discord
from discord.ext import commands
import dislash
from dislash import slash_commands, InteractionClient, Option, OptionType, OptionParam, SlashInteraction

# local modules
from pythonbot import PythonBot
from ._meme_generator import MemeGenerator
from utils import print_context


class Memes(commands.Cog, name='memes'):
    """
    create and send memes
    """

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.generator = MemeGenerator()

    @commands.command(
        name='skyrim',
        aliases=[],
        description='generate skyrim skill meme',
        help='generate skyrim skill meme',
    )
    @print_context
    async def skyrim_command(
            self,
            ctx: commands.Context,
            skill: str,
            level: str,
            *args: str,
    ) -> None:
        """
        generate and send skyrim skill meme
        """

        img_buf = self.generator.skyrim(skill, level)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(
        name='simply',
        aliases=[],
        description='generate simply meme',
        help='generate simply meme',
    )
    @print_context
    async def simply_command(self, ctx: commands.Context, *words: str) -> None:
        """
        generate and send simply meme
        """

        text = ' '.join(words)
        img_buf = self.generator.oneDoesNotSimply(text)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(
        name='aliens',
        aliases=[],
        description='generate aliens meme',
        help='generate aliens meme',
    )
    @print_context
    async def aliens_command(self, ctx: commands.Context, *words: str) -> None:
        """
        generate and send aliens meme
        """

        text = ' '.join(words)
        img_buf = self.generator.historyAliensGuy(text)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(
        name='buzz',
        aliases=['toystory'],
        description='generate and send buzz meme',
        help='generate and send buzz meme',
    )
    @print_context
    async def buzz_command(self, ctx: commands.Context, *text: str) -> None:
        """
        generate and send buzz meme
        """

        text = ' '.join(text)
        img_buf = await self.generator.toy_story_meme(text)
        file = discord.File(fp=img_buf, filename='image.png')
        await ctx.send(file=file)

    @slash_commands.is_owner()
    @slash_commands.slash_command(
        name='buzz',
        description='generate and send buzz meme',
    )
    async def buzz_slash(
            self,
            inter: dislash.MessageInteraction,
            text: str = OptionParam(
                default=None,
                name='text',
                description='the text for kaa to say',
            ),
    ) -> None:
        """
        generate and send buzz meme
        """

        buffer = await self.generator.toy_story_meme(text)
        file = discord.File(fp=buffer, filename='meme.png')
        await inter.reply('generating meme...')
        await inter.channel.send(file=file)
        await inter.delete()
