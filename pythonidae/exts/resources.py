# -*- coding: utf-8 -*-


# third-party modules - discord and related
#import discord
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

    @commands.group(case_insensitive=True, aliases=['py'])
    @print_context
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

        msg='''\
__**Python Reference Materials**__
:link: Python 3 Official Documentation <https://docs.python.org/3/>
:link: Python Notes for Professionals <https://books.goalkicker.com/PythonBook/>
:link: Learn Python in Y minutes <https://learnxinyminutes.com/docs/python/>
:link: Real Python <https://www.realpython.com/>'''
        await ctx.send(msg)

    @python.command(aliases=['path', 'studyorder'])
    @print_context
    async def curriculum(self, ctx: commands.Context) -> None:
        """python standard library curriculum"""

        msg = '''\
__**Python Standard Library - Reading order - Beginner**__
1) :link: Automate the Boring Stuff with Python, 2nd Edition: <https://automatetheboringstuff.com/> (free)
2) **One other beginner book to round out beginner knowledge, such as:**
    :link: Python Crash Course, 2nd Edition <https://nostarch.com/pythoncrashcourse2e>
    :link: Program Arcade Games With Python And Pygame <http://programarcadegames.com/> (free)
__**Python Standard Library - Video courses - Beginner**__
1) :link: Automate the Boring Stuff with Python Programming <https://www.udemy.com/course/automate/> (often free)
__**Python Standard Library - Reading order - Intermediate**__
1) :link: Python Tricks <https://realpython.com/products/python-tricks-book/>
2) :link: Effective Python, 2nd Edition <https://effectivepython.com/>
3) :link: Python Cookbook, 3rd Edition <http://shop.oreilly.com/product/0636920027072.do>
__**Python Standard Library - Books - Advanced**__
:link: Fluent Python <http://shop.oreilly.com/product/0636920032519.do>
:link: Problem Solving with Algorithms and Data Structures using Python <https://runestone.academy/runestone/books/published/pythonds/index.html> (free)
__**Python Standard Library - Video courses - Intermediate / Advanced**__
1) :link: Python 3: Deep Dive (Part 1 - Functional) <https://www.udemy.com/course/python-3-deep-dive-part-1/>
2) :link: Python 3: Deep Dive (Part 2 - Iteration, Generators) <https://www.udemy.com/course/python-3-deep-dive-part-2/>
3) :link: Python 3: Deep Dive (Part 3 - Hash Maps) <https://www.udemy.com/course/python-3-deep-dive-part-3/>
4) :link:  Python 3: Deep Dive (Part 4 - OOP) <https://www.udemy.com/course/python-3-deep-dive-part-4/>
__**Alternate download methods**__
:link: Library Genesis <http://gen.lib.rus.ec/>'''
        await ctx.send(msg)

    @python.command(aliases=['game_dev'])
    @print_context
    async def gamedev(self, ctx: commands.Context) -> None:
        """python game development resources"""

        msg = '''\
__**Pygame Resources**__
:link: Pygame - Documentation <https://www.pygame.org/docs/>
:link: Pygame GUI - Documentation <https://pygame-gui.readthedocs.io/en/latest/index.html>
:link: Pygame state engine example <https://gist.github.com/iminurnamez/8d51f5b40032f106a847>
:link: Pygame (color) Picker <https://github.com/GearPenguin/Pygame-Tests/blob/master/Picker.py> (find color names to use)
__**Game Dev Assets - Free**__
:link: Kenney Assets <https://kenney.nl/assets> (best)
:link: OpenGameArt <https://opengameart.org/>
__**Terminal-based game resources**__
:link: blessed <https://github.com/jquast/blessed> (python curses wrapper with enhancements)'''
        await ctx.send(msg)

    @python.command()
    @print_context
    async def vscode(self, ctx: commands.Context) -> None:
        """useful python vs code extensions"""

        msg = '''\
__**Helpful Visual Studio Code extensions**__
**Python Specific - Assorted**
Python - Microsoft (basically required for coding python in vs code)
Visual Studio IntelliCode - Microsoft (alternative to jedi/pylint etc)
Pylance - Microsoft (install alongside Intellicode
python-snippets - cstrap
**Python Specific - Qt**
PYQT Integration - Feng Zhou
Qt for Python - Sean Wu
**Assorted**
Code Runner - Jun Han (more convenient ways to run your code)
Settings Sync - Shan Khan (sync your settings across devices)
Google Search - adelphes (highlight and google search)
Live Share Extension Pack - Microsoft (collaborate in real time)
Transformer - dakara
Whitespace+ - David Houchin
**Git**
GitLens — Git supercharged - Eric Amodio (feature packed)
.gitignore Generator - Piotr Palarz
Git History - Don Jayamanne
**Themes**
Dracula Official - Dracula Theme'''
        await ctx.send(msg)

    @python.command()
    @print_context
    async def ides(self, ctx: commands.Context) -> None:
        """quality IDEs for python"""

        msg = '''\
__**Well liked IDEs for coding in Python**__
:link: Visual Studio Code <https://code.visualstudio.com/download> (free, fairly lightweight and extensible, my choice)
:link: PyCharm <https://www.jetbrains.com/pycharm/download/> (community edition is free, probably the best/easiest)
:link: Jupyter <https://jupyter.org/install> (good replacement for Python Interactive Shell)
:link: Spyder <https://docs.spyder-ide.org/installation.html> (Good for data science, made with Python)
:link: Sublime Text 3 <https://www.sublimetext.com/3> (unlimited free trial, crackable, fast, lightweight, and extensible)'''
        await ctx.send(msg)

    @python.command(aliases=['discord.py'])
    @print_context
    async def discord(self, ctx: commands.Context) -> None:
        """discord.py learning resources"""

        msg = '''\
__**discord.py resources**__
:link: discord.py documentation <https://discordpy.readthedocs.io/en/latest/>
:link: discord.ext.commands documentation <https://discordpy.readthedocs.io/en/latest/ext/commands/index.html>
:link: realpython discord bot tutorial <https://realpython.com/how-to-make-a-discord-bot-python/>
:link: discord.py cogs example <https://gist.github.com/OneEyedKnight/f0411f9a5e9dea23b96be0bf6dd86d2d>
:link: error handling cog example <https://gist.github.com/pauloLuz2002/15fa6e8807245f2f41644a767188bd0a>
**assorted other discord.py stuff**
:link: my discord python bot repo <https://github.com/haasosaurus/pythonidae/>
**async stuff (you need to know a little about async for making a discord bot)**
:link: python asyncio module docs <https://docs.python.org/3/library/asyncio.html>
:link: python & async simplified <https://www.aeracode.org/2018/02/19/python-async-simplified/>
:link: realpython - Async IO in Python: A Complete Walkthrough <https://realpython.com/async-io-python/>'''
        await ctx.send(msg)

    @python.command()
    @print_context
    async def snippets(self, ctx: commands.Context) -> None:
        """vs code python snippets"""

        text = '''\
{
    "shebang and coding": {
        "prefix": "shebang",
        "body": "#!/usr/bin/env python\\n# coding=utf-8\\n\\n\\n$0",
        "description": "adds shebang and coding lines"
    },
    "list comprehension": {
        "prefix": "lc",
        "body": "[${1:value} for ${2:value} in ${3:iterable}]$0",
        "description" : "List comprehension for creating a list based on existing lists."
    },
    "list comprehension if else": {
        "prefix": "lc.if_else",
        "body": "[${1:value} if ${2:condition} else ${3:condition} for ${4:value} in ${5:iterable}]$0",
        "description" : "List comprehension for creating a list based on existing lists, with conditional if-else statement."
    },
    "list comprehension if": {
        "prefix": "lc.if",
        "body": "[${1:value} for ${2:value} in ${3:iterable} if ${4:condition}$0]",
        "description" : "List comprehension for creating a list based on existing lists, with conditional if statement."
    },
    "list comprehension - nested": {
        "prefix": "lc.nested",
        "body": "[[${1:j} for ${2:j} in ${4:inner_iterable}] for ${5:i} in ${6:outer_iterable}]$0",
        "description" : "list comprehension - make list of lists"
    },
    "list comprehension - flatten": {
        "prefix": "lc.flatten",
        "body": "[${1:val} for ${2:sublist} in ${3:matrix} for ${4:val} in ${5:sublist}]$0",
        "description" : "list comprehension - flatten nested iterables"
    },
    "list comprehension - flatten - if": {
        "prefix": "lc.flattenif",
        "body": "[${1:val} for ${2:sublist} in ${3:matrix} for ${4:val} in ${5:sublist} if ${6:condition}]$0",
        "description": "list comprehension - flatten nested iterables - if"
    },
    "list comprehension - multiline string to lists of words": {
        "prefix": "lc.multiline_string_to_lists_of_words",
        "body": "[[${1:word} for ${2:word} in ${3:line}.split()] for ${4:line} in ${5:multiline_string}.split('\\n')]$0",
        "description": "list comprehension - multiline string to a list of lists of words"
    },
    "list comprehension - multiline file to lists of words": {
        "prefix": "lc.multiline_file_to_lists_of_words",
        "body": "[[${1:word} for ${2:word} in ${3:line}.split()] for ${4:line} in ${5:file_object}.readlines()]$0",
        "description": "list comprehension - multiline file to a list of lists of words"
    },
    "list comprehension - flatten - partially 2d array": {
        "prefix": "lc.flatten_partially_2d_array",
        "body": "[${1:x} for ${2:element} in ${3:partially_2d_array} for ${4:x} in (${5:element} if isinstance(${6:element}, list) else [${7:element}])]$0",
        "description": "list comprehension - flatten a partially 2d array"
    }
}'''
        p = commands.Paginator(prefix='```json', suffix='```')
        for line in text.split('\n'):
            p.add_line(line)
        for page in p.pages:
            await ctx.send(page)

    @commands.command()
    @print_context
    async def practice(self, ctx: commands.Context) -> None:
        """sites for practicing programming"""

        msg='''\
__**Python Practice Websites**__
:link: Project Euler <https://www.projecteuler.net/> (Math problems)
:link: LeetCode <https://www.leetcode.com/> (Preparing for technical interviews)
:link: binarysearch <https://binarysearch.com/>
:link: Codewars <https://www.codewars.com/>
:link: HackerRank <https://www.hackerrank.com/>
:link: CodeChef <https://www.codechef.com/>
:link: HackerEarth <https://www.hackerearth.com/>
:link: CodingBat <https://www.codingbat.com/python>
:link: CodeSignal <https://www.codesignal.com/>
:link: Exercism <https://www.exercism.io/>
:link: Topcoder <https://www.topcoder.com/>
:link: Advent of Code <https://adventofcode.com/>
:link: CSES Problem Set <https://cses.fi/problemset/list/>
:link: CodinGame <https://www.codingame.com/home>'''
        await ctx.send(msg)

    @commands.command(aliases=['gameprojects'])
    @print_context
    async def game_projects(self, ctx: commands.Context) -> None:
        """game project ideas"""

        msg = '''\
"Guess the number"
Hangman
Rock-Paper-Scissors (turn-based gameplay, opponent AI)
Tic-Tac-Toe (turn-based gameplay, opponent AI)
snake
breakout (Arkanoid) / Pong (collisions, stable frame rate, score, levels)
Tetris (data structures and how they relate to gaming)
1942 / Shoot-em-up (enemies, bullets)
simple platformer / pinball game if your engine does platformers (gravity-based collisions)
Bomberman / Pacman (tile-based movement, complex enemy AI)
Two-player game of any of the types above (two player inputs)
Roguelike / Diablo (Inventory management, multiple enemy AIs, saving and loading complex game states)
Faceball / Wolfenstein 3D (basic 3d movement and rendering)
Network turn-based game (basic networking)
Gimmicky 3D third-person platformer (physics, complex 3d movement)
Network real-time game (Client-server synchronism, lag)
MMORPG (Persistent world)'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def projects(self, ctx: commands.Context) -> None:
        """project idea resources"""

        msg = '''\
__**project ideas**__
:link: Mega Project List <https://github.com/karan/Projects> (very good)
:link: Python Project Ideas for 2020 <https://data-flair.training/blogs/python-project-ideas/>
:link: Intermediate Python Workshop/Projects <https://wiki.openhatch.org/wiki/Intermediate_Python_Workshop/Projects>'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def downloading(self, ctx: commands.Context) -> None:
        """helpful download sites"""

        msg = '''\
__**download links**__
:link: rarbg <https://rarbg.to/>
:link: btdigg <https://en.btdig.com/> (dht search)
:link: skytorrents <https://www.skytorrents.org/> (meta search)
:link: torrentz2 <https://torrentz2.eu/> (meta search)
:link: pirate bay <https://thepiratebay.org/>
:link: 1337x <https://1337x.to/>
:link: torrentdownloads <https://www.torrentdownloads.me/>
:link: limetorrents <https://www.limetorrents.cc/>
:link: zooqle <https://zooqle.com/>
:link: glodls <https://glodls.to/>
:link: demonoid <https://www.demonoid.is/>
:link: library genesis <http://gen.lib.rus.ec/> (ebooks)'''
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(Resources(bot))
