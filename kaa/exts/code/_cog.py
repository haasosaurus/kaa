# -*- coding: utf-8 -*-


# standard library modules
import pathlib
import re

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from kaantext import Kaantext
from utils import print_context
from ._codeformatter import CodeFormatter


class Code(commands.Cog, name='code'):
    """
    general code related commands
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

        # block command regex stuff
        pattern = r'''```.*?\n(.*?)```'''
        self.pattern = re.compile(pattern=pattern, flags=re.DOTALL)

        # markdown command
        self.markdown_text = None
        path = 'resources/data/text/code/markdown.md'
        with pathlib.Path(path).resolve().open('r') as f:
            self.markdown_text = f.read()

    async def format_content(
            self,
            content: str,
            language: str,
    ) -> str:
        """
        maybe this would be a good place to try out pattern matching
        """

        # format python
        if language in {'py', 'python'}:
            content = CodeFormatter.python(content)

        # format xml
        elif language in {'xml', 'html', 'xhtml'}:
            content = CodeFormatter.xml(content)

        # format objective c
        elif language in {'objc', 'objectivec'}:
            content = CodeFormatter.objective_c(content)

        # format c
        elif language in {'c'}:
            content = CodeFormatter.c(content)

        # format c++
        elif language in {'cpp', 'c++'}:
            content = CodeFormatter.cpp(content)

        # format c#
        elif language in {'cs', 'csharp'}:
            content = CodeFormatter.cs(content)

        # format java
        elif language in {'java'}:
            content = CodeFormatter.java(content)

        # format javascript/typescript
        elif language in {'javascript', 'js', 'typescript', 'ts'}:
            content = CodeFormatter.javascript(content)

        # format css
        elif language in {'css'}:
            content = CodeFormatter.css(content)

        return content

    @commands.command(
        name='block',
        aliases=['format'],
        description='blocks/formats target message code',
        help='''\
resend a message as a codeblock with syntax highlighting
formats supported languages if specified
if block indexes not specified it will send all blocks'''
    )
    @commands.guild_only()
    @print_context
    async def block_command(
            self,
            ctx: Kaantext,
            message: discord.Message,
            language: str = '',
            *block_indexes: int,
    ) -> None:
        """
        resend a message as a codeblock with syntax highlighting
        formats supported languages if specified
        if block indexes not specified it will send all blocks
        """

        content = message.clean_content

        # check if there's any existing codeblocks
        blocks = self.pattern.findall(content)

        # otherwise use whole message
        if not blocks:
            blocks.append(content)

        # format and block all if no indexes specified
        if not block_indexes:
            block_indexes = range(len(blocks))

        # send all the blocks
        for index in block_indexes:
            if index in range(len(blocks)):
                content = blocks[index]
                content = await self.format_content(content, language)
                msg = f'```{language}\n{content}\n```'
                await ctx.send(msg)

    @commands.command(
        name='markdown',
        aliases=['md'],
        description='sends markdown instructions',
        help='sends instructions for commonly used markdown: codeblock, syntax highlighting, and spoilers',
    )
    async def markdown_command(self, ctx: Kaantext):
        """
        sends instructions for commonly used markdown:
        codeblock, syntax highlighting, and spoilers
        """

        await ctx.send(self.markdown_text)
