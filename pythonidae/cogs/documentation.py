# coding=utf-8


# standard library modules
import argparse, asyncio
import base64, bisect, builtins
import codecs, collections, contextlib, copy, csv
import datetime, decimal
import enum
import fileinput, fractions, functools
import gc, getpass
import inspect, itertools
import json
import locale, logging
import math
import numbers
import operator, os
import pathlib, pickle, pprint
import random
import re
import secrets, shlex, signal, sqlite3, statistics, string
import this, time, timeit, traceback, typing, types
import weakref

# standard library modules - typing
from typing import List, Type

# third-party modules
import matplotlib, matplotlib.pyplot, more_itertools
import netifaces, numpy
import pandas, PIL, PIL.ImageDraw, pretty_help, pyautogui
import requests
import sortedcontainers, sqlalchemy
import tqdm

# third-party modules - broken
#import scapy.all

# third-party modules - pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame_sdl2

# third-party modules - discord and related
import discord, discord_argparse
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class DocumentationCog(commands.Cog, name='documentation'):
    """python documentation commands"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.modules = {
            # standard library modules
            'argparse': argparse, 'asyncio': asyncio,
            'base64': base64, 'bisect': bisect, 'builtins': builtins,
            'codecs': codecs, 'collections': collections,
            'contextlib': contextlib, 'copy': copy, 'csv': csv,
            'datetime': datetime, 'decimal': decimal,
            'enum': enum,
            'fileinput': fileinput, 'fractions': fractions,
            'functools': functools,
            'gc': gc, 'getpass': getpass,
            'inspect': inspect, 'itertools': itertools,
            'json': json,
            'locale': locale, 'logging': logging,
            'math': math,
            'numbers': numbers,
            'operator': operator, 'os': os,
            'pathlib': pathlib, 'pickle': pickle, 'pprint': pprint,
            'random': random, 're': re,
            'secrets': secrets, 'shlex': shlex, 'signal': signal,
            'sqlite': sqlite3, 'statistics': statistics, 'string': string,
            'time': time, 'timeit': timeit, 'traceback': traceback,
            'types': types, 'typing': typing,
            'weakref': weakref,

            # third-party modules
            'matplotlib': matplotlib, 'more_itertools': more_itertools,
            'netifaces': netifaces, 'numpy': numpy,
            'pandas': pandas, 'PIL': PIL, 'pretty_help': pretty_help,
            'pyautogui': pyautogui,
            'requests': requests,
            'sortedcontainers': sortedcontainers, 'sqlalchemy': sqlalchemy,
            'tqdm': tqdm,

            # third-party modules - broken
            #'scapy.all': scapy.all,

            # third-party modules - pygame
            'pygame': pygame, 'pygame_sdl2': pygame_sdl2,

            # third-party modules - discord and related
            'discord': discord, 'discord.ext.commands': commands,
            'discord_argparse': discord_argparse,
        }
        self.module_aliases = {
            'commands': 'discord.ext.commands',
            'ni': 'netifaces',
            'np': 'numpy',
            'pd': 'pandas',
            'py': 'builtins', 'python': 'builtins',
            'scapy': 'scapy.all',
        }
        self.hidden_modules = {
            'pygame_sdl2'
        }
        self.module_names = sorted(x for x in self.modules if x not in self.hidden_modules)

    @commands.command(
        aliases=['documentation', 'doc', 'pydoc', 'pydocs']
    )
    @print_context
    async def docs(
            self,
            ctx: commands.Context,
            *members: str,
    ) -> None:
        """python documentation"""

        errored = False
        module = None
        members = collections.deque(x for y in members for x in y.split('.'))
        if members:
            module = members.popleft()
        else:
            error_msg = 'missing module argument'
            errored = True
        module = self.module_aliases.get(module, module)
        if not errored and module not in self.modules:
            error_msg = f"module '{module}' is unsupported"
            errored = True
        if errored:
            await self.bot.send_error_msg(ctx, error_msg)
            await self.send_supported_modules(ctx)
            await self.send_usage(ctx)
            return

        target_name = module
        target = self.modules[target_name]

        while members:
            member_name = members.popleft()
            if member_name not in dir(target):
                error_msg = f"'{target_name}' has no member '{member_name}'"
                self.bot.send_error_msg(ctx, error_msg)
                member_list_header = f"**`{target_name}'s members:`**"
                member_list = await self.make_members_list(target, target_name)
                await ctx.send(member_list_header)
                await self.send_members(ctx, member_list)
                await self.send_usage(ctx)
                return
            member = getattr(target, member_name)
            target_name = member_name
            target = member

        if not target:
            error_msg = f"failed to get docs for '{target_name}', sorry about that..."
            await self.bot.send_error_msg(error_msg)
            return

        await self.send_docs_and_methods(ctx, target, target_name, '', '')

    async def send_supported_modules(self, ctx: commands.Context) -> None:
        """sends supported modules list to ctx"""

        await self.send_members(
            ctx,
            self.module_names,
            title='Currently available modules:'
        )

    async def send_usage(self, ctx: commands.Context) -> None:
        """send usage information"""

        usage = '**`Usage: !docs module[.| ]members...`**'
        await self.bot.send_info_msg(ctx, usage)





    async def send_docs_and_methods(
            self,
            ctx: commands.Context,
            target,
            target_name: str,
            obj=None,  # str
            method=None  # str
    ) -> None:
        """final method to send everything"""

        docs = await self.make_docs(target, target_name, obj, method)
        if not docs:
            error_msg = f'**`ERROR: docs for {target_name} not found, sorry`**'
            await ctx.send(error_msg)
            return
        method_list = await self.make_members_list(target, target_name)
        await self.send_docs(ctx, docs)
        if method_list:
            await self.send_members(ctx, method_list, title='Methods:')

    async def make_docs(
            self,
            target,
            target_name: str,
            obj=None,
            method=None
    ) -> str:
        """make the docs and return it as a string"""

        if obj:
            docs_sig_begin = f'{obj}'
        else:
            docs_sig_begin = target_name
        if method:
            docs_sig_begin += '.' + method
        docs = ''

        try:
            docs_sig = str(inspect.signature(target))
            docs_body = inspect.getdoc(target)
            docs = docs_sig_begin + docs_sig + '\n\n' + docs_body
        except (ValueError, TypeError):
            docs_sig = docs_sig_begin + '(?)'
            docs_body = inspect.getdoc(target)
            if docs_body:
                if (target_name + '(') not in docs_body:
                    docs = docs_sig + '\n\n'
                docs = docs_body
            else:
                return ''
        return docs

    async def make_members_list(self, obj, obj_name: str) -> list:
        """return a list of all the public members of an objest"""

        if hasattr(obj, '__dict__'):
            members = vars(obj)
        else:
            members = dir(obj)
        private_or_upper = lambda x: any((x.startswith('__'), x.isupper()))
        if obj == builtins:
            exp = lambda x: type(vars(builtins)[x]) == type and issubclass(vars(builtins)[x], BaseException)
            member_list = [x for x in members if not private_or_upper(x) and not exp(x)]
        else:
            member_list = [x for x in members if not private_or_upper(x)]
        return tuple(member_list)

    async def send_docs(self, ctx, docs: str) -> None:
        """send documenation string, slicing it if needed"""

        if len(docs) < 1900:
            await ctx.send('```\n' + docs + '```')
        else:
            docs_list = docs.strip().split('\n')
            slices = 2
            docs_slices = None
            while True:
                docs_list_slices = more_itertools.sliced(
                    docs_list,
                    len(docs_list) // slices
                )
                docs_slices = ['\n'.join(x) for x in docs_list_slices]
                if all(len(x) < 1990 for x in docs_slices):
                    break
                slices += 1
            for docs in docs_slices:
                if not docs.isspace():
                    msg = '```\n' + docs + '```'
                    await ctx.send(msg)

    async def send_members(
            self,
            ctx: commands.Context,
            msg_list: list,
            title: str = None
    ) -> None:
        """send list of an object's members, slicing it if needed"""

        msg_list = sorted(msg_list, key=lambda x: x.lower())
        if title:
            msg_list.insert(0, title + '\n\n')
        msg = '```\n' + '  '.join(msg_list) + '```'
        if len(msg) < 1990:
            await ctx.send(msg)
        else:
            slices = 2
            msg_slices = None
            while True:
                msg_list_slices = more_itertools.sliced(
                    msg_list,
                    len(msg_list) // slices
                )
                msg_slices = ['  '.join(x) for x in msg_list_slices]
                if all(len(x) < 1970 for x in msg_slices):
                    break
                slices += 1
            for msg in msg_slices:
                msg = '```\n' + msg + '```'
                await ctx.send(msg)

    @commands.command(hidden=True)
    @print_context
    async def this(self, ctx: commands.Context) -> None:
        """send this"""

        msg = '```\n' + codecs.decode(this.s, 'rot13') + '```'
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(DocumentationCog(bot))
