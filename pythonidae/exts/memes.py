# -*- coding: utf-8 -*-


# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from memegenerator import MemeGenerator
from utils import print_context


class Memes(commands.Cog, name='memes'):# coding=utf-8
    """commands for sending memes"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.generator = MemeGenerator()

    @commands.command(usage='!skill SKILL LEVEL')
    @print_context
    async def skyrim(
            self,
            ctx: commands.Context,
            skill: str,
            level: str,
            *args: str,
    ) -> None:
        """!skyrim SKILL LEVEL"""

        img_buf = self.generator.skyrim(skill, level)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(usage='!simply *WORDS')
    @print_context
    async def simply(self, ctx: commands.Context, *words: str) -> None:
        """!simply *WORDS"""

        text = ' '.join(words)
        img_buf = self.generator.oneDoesNotSimply(text)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(usage='!aliens *WORDS')
    @print_context
    async def aliens(self, ctx: commands.Context, *words: str) -> None:
        """!aliens *WORDS"""

        text = ' '.join(words)
        img_buf = self.generator.historyAliensGuy(text)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

    @commands.command(aliases=['buzz'], usage='!toystory *WORDS')
    @print_context
    async def toystory(self, ctx: commands.Context, *words: str) -> None:
        """!toystory *WORDS"""

        text = ' '.join(words)
        img_buf = self.generator.toyStoryMeme(text)
        await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Memes(bot))
