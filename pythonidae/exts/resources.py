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

    @commands.group(case_insensitive=True, aliases=['py'])
    async def python(self, ctx: commands.Context) -> None:
        """python specific resource sub-commands"""

        if ctx.invoked_subcommand is None:
            msg = (
                'for more information, use `!help python`\n'
                'for sub-commands use `!python SUBCOMMAND`'
            )
            await self.bot.send_info_msg(ctx, msg)

    @python.command(aliases=['ref', 'refs'])
    @print_context
    async def reference(self, ctx: commands.Context) -> None:
        """python reference material"""

        msg = self.resource_texts['reference']
        await ctx.send(msg)

    @python.command(aliases=['path', 'studyorder'])
    @print_context
    async def curriculum(self, ctx: commands.Context) -> None:
        """python standard library curriculum"""

        msg = self.resource_texts['curriculum']
        await ctx.send(msg)

    @python.command(aliases=['game_dev'])
    @print_context
    async def gamedev(self, ctx: commands.Context) -> None:
        """python game development resources"""

        msg = self.resource_texts['gamedev']
        await ctx.send(msg)

    @python.command()
    @print_context
    async def vscode(self, ctx: commands.Context) -> None:
        """useful python vs code extensions"""

        msg = self.resource_texts['vscode']
        await ctx.send(msg)

    @python.command()
    @print_context
    async def ides(self, ctx: commands.Context) -> None:
        """quality IDEs for python"""

        msg = self.resource_texts['ides']
        await ctx.send(msg)

    @python.command(aliases=['discord.py'])
    @print_context
    async def discord(self, ctx: commands.Context) -> None:
        """discord.py learning resources"""

        msg = self.resource_texts['discord']
        await ctx.send(msg)

    @python.command()
    @print_context
    async def snippets(self, ctx: commands.Context) -> None:
        """vs code python snippets"""

        msg = self.resource_texts['snippets']
        p = commands.Paginator(prefix='```json', suffix='```')
        for line in msg.split('\n'):
            p.add_line(line)
        for page in p.pages:
            await ctx.send(page)

    @commands.command()
    @print_context
    async def practice(self, ctx: commands.Context) -> None:
        """sites for practicing programming"""

        msg = self.resource_texts['practice']
        await ctx.send(msg)

    @commands.command(aliases=['gameprojects'])
    @print_context
    async def game_projects(self, ctx: commands.Context) -> None:
        """game project ideas"""

        msg = self.resource_texts['game_projects']
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def projects(self, ctx: commands.Context) -> None:
        """project idea resources"""

        msg = self.resource_texts['projects']
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def downloading(self, ctx: commands.Context) -> None:
        """helpful download sites"""

        msg = self.resource_texts['downloading']
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Resources(bot))
