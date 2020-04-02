# coding=utf-8


import os

# import discord
from discord.ext import commands
from googleapiclient import discovery

from utils import print_context


class ResourceCog(commands.Cog, name='Resource Commands'):
    """
    original purpose:
    someday it will take resources and their categories as input
    give resources based on search categories

    currently temporary hardcoded resource links due to people
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(help='!save_resource CATEGORY URL')
    @print_context
    async def resource_save(
            self,
            ctx: commands.Context,
            category: str = None,
            link: str = None
    ) -> None:
        """save link to resources"""

        if not link:
            error_msg = '**`Link and/or Category Missing - Link not saved`**'
            usage = '**`Usage: !save_resource CATEGORY URL`**'
            await ctx.send(error_msg)
            await ctx.send(usage)
            return

        # need to check that the resource isn't already there?
        category = category.lower()
        service = discovery.build(
            'sheets',
            'v4',
            credentials=None
        )
        spreadsheet_id = os.getenv('SPREADSHEET_ID')
        request = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A2:C',
            majorDimension='ROWS'
        )
        response = request.execute()

        # get last row of google sheet to prevent overwriting
        lastrow = len(response['values'])
        new_values = [[link, category, str(ctx.author)]]
        new_body = {'values' : new_values}
        new_range = 'A' + str(lastrow + 2) + ':C'
        update_request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=new_range,
            valueInputOption='RAW',
            body=new_body
        )
        update_request.execute()

        await ctx.send('Link successfully saved to ' + category + '!')

    @commands.command()
    @print_context
    async def reference(self, ctx: commands.Context) -> None:
        """display python reference links"""

        msg='''\
__**Python Reference Materials**__
:link: Python 3 Official Documentation <https://docs.python.org/3/>
:link: Python Notes for Professionals <https://books.goalkicker.com/PythonBook/>
:link: Learn Python in Y minutes <https://learnxinyminutes.com/docs/python/>
:link: Real Python <https://www.realpython.com/>\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def curriculum(self, ctx: commands.Context) -> None:
        """display python standard library curriculum"""

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
:link: Library Genesis <http://gen.lib.rus.ec/>\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def practice(self, ctx: commands.Context) -> None:
        """display list of websites for practicing python"""

        msg='''\
__**Python Practice Websites**__
:link: Project Euler <https://www.projecteuler.net/> (Math problems)
:link: LeetCode <https://www.leetcode.com/> (Preparing for technical interviews)
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
:link: CodinGame <https://www.codingame.com/home>\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def gamedev(self, ctx: commands.Context) -> None:
        """display python game development resources"""

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
:link: blessed <https://github.com/jquast/blessed> (python curses wrapper with enhancements)\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def vscode(self, ctx: commands.Context) -> None:
        """display some useful vs code extensions"""

        msg = '''\
__**Helpful Visual Studio Code extensions**__
**Python Specific - Assorted**
Python - Microsoft (basically required for coding python in vs code)
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
Dracula Official - Dracula Theme
**Advanced** (don't use unless you're good at troubleshooting)
Visual Studio IntelliCode - Microsoft (alternative to jedi/pylint etc)\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def ides(self, ctx: commands.Context) -> None:
        """display list of quality IDEs"""

        msg = '''\
__**Well liked IDEs for coding in Python**__
:link: Visual Studio Code <https://code.visualstudio.com/download> (free, fairly lightweight and extensible, my choice)
:link: PyCharm <https://www.jetbrains.com/pycharm/download/> (community edition is free, probably the best/easiest)
:link: Jupyter <https://jupyter.org/install> (good replacement for Python Interactive Shell)
:link: Spyder <https://docs.spyder-ide.org/installation.html> (Good for data science, made with Python)
:link: Sublime Text 3 <https://www.sublimetext.com/3> (unlimed free trial, crackable, fast, lightweight, and extensible)\
'''
        await ctx.send(msg)

    @commands.command()
    @print_context
    async def projects(self, ctx: commands.Context) -> None:
        """display project idea resources"""

        msg = '''\
:link: Mega Project List <https://github.com/karan/Projects> (very good)
:link: Python Project Ideas for 2020 <https://data-flair.training/blogs/python-project-ideas/>
:link: Intermediate Python Workshop/Projects <https://wiki.openhatch.org/wiki/Intermediate_Python_Workshop/Projects>\
'''
        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ResourceCog(bot))
