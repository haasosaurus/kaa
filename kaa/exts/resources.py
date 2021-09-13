# -*- coding: utf-8 -*-


# standard library modules
import pathlib

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context, load_texts


class Resources(commands.Cog, name='resources'):
    """
    resource commands
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

        # text data
        text_paths = {
            'practice': 'resources/data/text/resources/practice.md',
            'game_projects': 'resources/data/text/resources/game_projects.md',
            'projects': 'resources/data/text/resources/projects.md',
            'downloading': 'resources/data/text/resources/downloading.md',
        }
        self.resource_texts = load_texts(text_paths)

    @commands.command(
        name='practice',
        aliases=[],
        description='sites for practicing',
        help='sites for practicing programming'
    )
    @print_context
    async def practice_command(self, ctx: Kaantext) -> None:
        """
        sites for practicing programming
        """

        msg = self.resource_texts['practice']
        await ctx.send(msg)

    @commands.command(
        name='game_projects',
        aliases=['gameprojects'],
        description='game project ideas',
        help='game project ideas',
    )
    @print_context
    async def game_projects_command(self, ctx: Kaantext) -> None:
        """
        game project ideas
        """

        msg = self.resource_texts['game_projects']
        await ctx.send(msg)

    @commands.command(
        name='projects',
        aliases=[],
        description='project idea resources',
        help='project idea resources',
    )
    @print_context
    async def projects_command(self, ctx: Kaantext) -> None:
        """
        project idea resources
        """

        msg = self.resource_texts['projects']
        await ctx.send(msg)

    @commands.command(
        name='downloading',
        aliases=[],
        description='helpful download sites',
        help='helpful download sites',
    )
    @print_context
    async def downloading_command(self, ctx: Kaantext) -> None:
        """
        helpful download sites
        """

        msg = self.resource_texts['downloading']
        await ctx.send(msg)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Resources(bot))
