# -*- coding: utf-8 -*-


# standard library modules
import pathlib

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Resources(commands.Cog, name='resources'):
    """
    resource commands
    """

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

        # text data
        self.resource_texts = {}
        text_paths = {
            'reference': 'resources/data/text/resources/reference.md',
            'curriculum': 'resources/data/text/resources/curriculum.md',
            'gamedev': 'resources/data/text/resources/gamedev.md',
            'vscode': 'resources/data/text/resources/vscode.md',
            'ides': 'resources/data/text/resources/ides.md',
            'discord': 'resources/data/text/resources/discord.md',
            'snippets': 'resources/data/text/resources/snippets.json',
            'practice': 'resources/data/text/resources/practice.md',
            'game_projects': 'resources/data/text/resources/game_projects.md',
            'projects': 'resources/data/text/resources/projects.md',
            'downloading': 'resources/data/text/resources/downloading.md',
        }
        self.load_texts(text_paths)

    def load_texts(self, text_paths: dict) -> None:
        """
        loads text data from text files
        """

        for name, path in text_paths.items():
            with pathlib.Path(path).resolve().open('r') as f:
                self.resource_texts[name] = f.read()

    @commands.group(
        name='python',
        aliases=['py'],
        description='python resource command group',
        help='python specific resource command group',
        invoke_without_command=True,
        case_insensitive=True,
    )
    async def python_command_group(self, ctx: commands.Context) -> None:
        """
        python specific resource command group
        """

        await ctx.send_help(ctx.command)

    @python_command_group.command(
        name='reference',
        aliases=[],
        description='python reference materials',
        help='python specific reference materials',
        )
    @print_context
    async def reference_command(self, ctx: commands.Context) -> None:
        """
        python specific reference materials
        """

        msg = self.resource_texts['reference']
        await ctx.send(msg)

    @python_command_group.command(
        name='path',
        aliases=['curriculum'],
        description='python standard lib curriculum',
        help='python specific standard library curriculum',
    )
    @print_context
    async def path_command(self, ctx: commands.Context) -> None:
        """
        python specific standard library curriculum
        """

        msg = self.resource_texts['curriculum']
        await ctx.send(msg)

    @python_command_group.command(
        name='gamedev',
        aliases=['game_dev'],
        description='python game dev resources',
        help='python specific game development resources',
    )
    @print_context
    async def gamedev_command(self, ctx: commands.Context) -> None:
        """
        python specific game development resources
        """

        msg = self.resource_texts['gamedev']
        await ctx.send(msg)

    @python_command_group.command(
        name='vscode',
        aliases=['vs_code'],
        description='useful python vs code extensions',
        help='python specific (mostly) useful vs code extensions',
    )
    @print_context
    async def vscode_command(self, ctx: commands.Context) -> None:
        """
        python specific (mostly) useful vs code extensions
        """

        msg = self.resource_texts['vscode']
        await ctx.send(msg)

    @python_command_group.command(
        name='ides',
        aliases=[],
        description='standard python ides',
        help='standard python ides',
    )
    @print_context
    async def ides_command(self, ctx: commands.Context) -> None:
        """
        standard python ides
        """

        msg = self.resource_texts['ides']
        await ctx.send(msg)

    @python_command_group.command(
        name='discord',
        aliases=['discord.py', 'discordpy', 'nextcord'],
        description='python discord bot resources',
        help='python discord bot resources',
    )
    @print_context
    async def discord_command(self, ctx: commands.Context) -> None:
        """
        python discord bot resources
        """

        msg = self.resource_texts['discord']
        await ctx.send(msg)

    @python_command_group.command(
        name='snippets',
        aliases=[],
        description='vs code python snippets',
        help='vs code python snippets',
    )
    @print_context
    async def snippets_command(self, ctx: commands.Context) -> None:
        """
        vs code python snippets
        """

        msg = self.resource_texts['snippets']
        p = commands.Paginator(prefix='```json', suffix='```')
        for line in msg.split('\n'):
            p.add_line(line)
        for page in p.pages:
            await ctx.send(page)

    @commands.command(
        name='practice',
        aliases=[],
        description='sites for practicing',
        help='sites for practicing programming'
    )
    @print_context
    async def practice_command(self, ctx: commands.Context) -> None:
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
    async def game_projects_command(self, ctx: commands.Context) -> None:
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
    async def projects_command(self, ctx: commands.Context) -> None:
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
    async def downloading_command(self, ctx: commands.Context) -> None:
        """
        helpful download sites
        """

        msg = self.resource_texts['downloading']
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Resources(bot))
