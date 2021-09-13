# -*- coding: utf-8 -*-


# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context, load_texts


class Python(commands.Cog, name='python'):
    """
    python specific commands
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

        # text data
        text_paths = {
            'reference': 'resources/data/text/resources/reference.md',
            'curriculum': 'resources/data/text/resources/curriculum.md',
            'gamedev': 'resources/data/text/resources/gamedev.md',
            'vscode': 'resources/data/text/resources/vscode.md',
            'ides': 'resources/data/text/resources/ides.md',
            'discord': 'resources/data/text/resources/discord.md',
            'snippets': 'resources/data/text/resources/snippets.json',
        }
        self.resource_texts = load_texts(text_paths)

    @commands.command(
        name='reference',
        aliases=[],
        description='python reference materials',
        help='python specific reference materials',
        )
    @print_context
    async def reference_command(self, ctx: Kaantext) -> None:
        """
        python specific reference materials
        """

        msg = self.resource_texts['reference']
        await ctx.send(msg)

    @commands.command(
        name='path',
        aliases=['curriculum'],
        description='python standard lib curriculum',
        help='python specific standard library curriculum',
    )
    @print_context
    async def path_command(self, ctx: Kaantext) -> None:
        """
        python specific standard library curriculum
        """

        msg = self.resource_texts['curriculum']
        await ctx.send(msg)

    @commands.command(
        name='gamedev',
        aliases=['game_dev'],
        description='python game dev resources',
        help='python specific game development resources',
    )
    @print_context
    async def gamedev_command(self, ctx: Kaantext) -> None:
        """
        python specific game development resources
        """

        msg = self.resource_texts['gamedev']
        await ctx.send(msg)

    @commands.command(
        name='vscode',
        aliases=['vs_code'],
        description='useful python vs code extensions',
        help='python specific (mostly) useful vs code extensions',
    )
    @print_context
    async def vscode_command(self, ctx: Kaantext) -> None:
        """
        python specific (mostly) useful vs code extensions
        """

        msg = self.resource_texts['vscode']
        await ctx.send(msg)

    @commands.command(
        name='ides',
        aliases=[],
        description='standard python ides',
        help='standard python ides',
    )
    @print_context
    async def ides_command(self, ctx: Kaantext) -> None:
        """
        standard python ides
        """

        msg = self.resource_texts['ides']
        await ctx.send(msg)

    @commands.command(
        name='discord',
        aliases=['discord.py', 'discordpy', 'nextcord'],
        description='python discord bot resources',
        help='python discord bot resources',
    )
    @print_context
    async def discord_command(self, ctx: Kaantext) -> None:
        """
        python discord bot resources
        """

        msg = self.resource_texts['discord']
        await ctx.send(msg)

    @commands.command(
        name='snippets',
        aliases=[],
        description='vs code python snippets',
        help='vs code python snippets',
    )
    @print_context
    async def snippets_command(self, ctx: Kaantext) -> None:
        """
        vs code python snippets
        """

        msg = self.resource_texts['snippets']
        p = commands.Paginator(prefix='```json', suffix='```')
        for line in msg.split('\n'):
            p.add_line(line)
        for page in p.pages:
            await ctx.send(page)


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Python(bot))
