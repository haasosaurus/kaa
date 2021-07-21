# -*- coding: utf-8 -*-


# standard library modules
import argparse, asyncio
import base64, bisect, builtins
import codecs, collections, contextlib, copy, csv
import datetime, decimal
import enum
import fileinput, fractions, functools
import gc, getpass
import inspect, io, itertools
import json
import locale, logging
import math
import numbers
import operator, os
import pathlib, pickle, pprint
import random
import re
import secrets, shlex, signal, sqlite3, statistics, string, sys
with contextlib.redirect_stdout(None):
    import this
import tkinter, time, timeit, traceback, typing, types
import weakref

# standard library modules - typing
from typing import List, Type

# third-party modules
import aioitertools, asyncstdlib
import dateparser
import matplotlib, matplotlib.pyplot, more_itertools
import netifaces, numpy
import pandas, PIL, PIL.ImageDraw, pretty_help, pytz
#import pyautogui
import requests
import sortedcontainers, sqlalchemy
import tqdm, tweepy

# third-party modules - broken
#import scapy.all

# third-party modules - pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, pygame_sdl2

# third-party modules - discord and related
import discord, discord_argparse
from discord.ext import commands
import dislash

# local modules
from pythonbot import PythonBot
from utils import print_context


class DocumentationCog(commands.Cog, name='documentation'):
    """python documentation commands"""

    member_kind_titles_sort_order = {
        # class specific titles and sort order
        'methods': ('Methods', 6),
        'methods_private': ('Methods (private)', 7),
        'methods_class': ('Methods (class)', 8),
        'methods_class_private': ('Methods (class) (private)', 9),
        'methods_static': ('Methods (static)', 10),
        'methods_static_private': ('Methods (static) (private)', 11),
        'properties': ('Properties', 12),
        'properties_private': ('Properties (private)', 13),

        # pygame titles and sort order
        'constants': ('Constants', 17),

        # all other titles and sort order
        'modules': ('Modules', 0),
        'modules_private': ('Modules (private)', 1),
        'classes': ('Classes', 2),
        'classes_private': ('Classes (private)', 3),
        'functions': ('Functions', 4),
        'functions_private': ('Functions (private)', 5),
        'exceptions': ('Exceptions', 14),
        'data': ('Data', 15),
        'data_private': ('Data (private)', 16),
        'dunders': ('Dunders', 18),
    }
    docs_blacklist_text = [
        'The MIT License (MIT)',
    ]

    @classmethod
    async def member_kind_title(cls, kind: str) -> str:
        """return member kind's title for output formatting"""

        title_order = cls.member_kind_titles_sort_order.get(kind)
        if title_order is None:
            title = f"Error: member kind '{kind}' missing title and order"
            print(title)
        else:
            title = title_order[0]
        return title

    @classmethod
    async def member_kind_sort_order(cls, kind: str) -> int:
        """return member kind's sort order for output formatting"""

        title_order = cls.member_kind_titles_sort_order.get(kind)
        if title_order is None:
            order = 0
            error_msg = f"Error: member kind '{kind}' missing title and order"
            print(error_msg)
        else:
            order = title_order[1]
        return order

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
            'inspect': inspect, 'io': io, 'itertools': itertools,
            'json': json,
            'locale': locale, 'logging': logging,
            'math': math,
            'numbers': numbers,
            'operator': operator, 'os': os,
            'pathlib': pathlib, 'pickle': pickle, 'pprint': pprint,
            'random': random, 're': re,
            'secrets': secrets, 'shlex': shlex, 'signal': signal,
            'sqlite': sqlite3, 'statistics': statistics, 'string': string,
            'sys': sys,
            'tkinter': tkinter, 'time': time, 'timeit': timeit,
            'traceback': traceback, 'types': types, 'typing': typing,
            'weakref': weakref,

            # third-party modules
            'aioitertools': aioitertools, 'asyncstdlib': asyncstdlib,
            'dateparser': dateparser,
            'matplotlib': matplotlib, 'more_itertools': more_itertools,
            'netifaces': netifaces, 'numpy': numpy,
            'pandas': pandas, 'PIL': PIL, 'pretty_help': pretty_help,
            #'pyautogui': pyautogui,
            'pytz': pytz,
            'requests': requests,
            'sortedcontainers': sortedcontainers, 'sqlalchemy': sqlalchemy,
            'tqdm': tqdm, 'tweepy': tweepy,

            # third-party modules - broken
            #'scapy.all': scapy.all,

            # third-party modules - pygame
            'pygame': pygame, 'pygame_sdl2': pygame_sdl2,

            # third-party modules - discord and related
            'discord': discord, 'discord.ext.commands': commands,
            'discord_argparse': discord_argparse,
            'dislash': dislash,
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
            'pygame_sdl2',
        }
        self.supported_modules = {
            'title': 'Supported Modules',
            'members': sorted(x for x in self.modules if x not in self.hidden_modules),
        }

    @commands.command(aliases=['documentation', 'doc', 'pydoc', 'docs'])
    @print_context
    async def pydocs(
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
                await ctx.send(member_list_header)
                await self.send_members(ctx, target)
                await self.send_usage(ctx)
                return
            member = getattr(target, member_name)
            target_name = member_name
            target = member

        if not target:
            error_msg = f"failed to get docs for '{target_name}', sorry about that..."
            await self.bot.send_error_msg(error_msg)
            return

        await self.send_docs_and_members(ctx, target, target_name, '', '')

    async def send_usage(self, ctx: commands.Context) -> None:
        """send usage information"""

        usage = '**`Usage: !docs module[.| ]members...`**'
        await self.bot.send_info_msg(ctx, usage)

    async def make_docs(
            self,
            target,
            target_name: str,
            obj=None,
            method=None
    ) -> List[str]:
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
                docs = ''

        # convert docs from string to list of lines (strings)
        docs = docs.strip()
        lines = []
        if docs:

            # check that docs not in list of known incorrects
            for text in DocumentationCog.docs_blacklist_text:
                if docs.startswith(text):
                    break
            else:
                lines = docs.split('\n')

        return lines

    async def send_docs_and_members(
            self,
            ctx: commands.Context,
            target,
            target_name: str,
            obj=None,  # str
            method=None  # str
    ) -> None:
        """final method to send everything"""

        # docs
        lines = await self.make_docs(target, target_name, obj, method)
        if not lines:
            error_msg = f"Docs for '{target_name}' not found, attempting to get members..."
            await self.bot.send_error_msg(ctx, error_msg)
        await self.send_docs(ctx, lines)

        # members
        await self.send_members(ctx, target)

    async def send_docs(self, ctx: commands.Context, lines: List[str]) -> None:
        """paginate lines of docs and send the pages"""

        pages = await self.paginate_lines(lines)
        await self.send_pages(ctx, pages)

    async def send_members(self, ctx: commands.Context, target) -> None:
        """analyze members, paginate, and send pages"""

        member_kinds = await self.analyze_members(target)
        lines = await self.format_member_kinds(member_kinds)
        pages = await self.paginate_lines(lines)
        await self.send_pages(ctx, pages)

    async def analyze_members(self, obj: object) -> dict:
        """choose method to analyze and object's members with"""

        if inspect.isclass(obj):
            return await self.analyze_class_members(obj)
        else:
            return await self.analyze_object_members(obj)

    async def analyze_class_members(self, class_object: Type) -> dict:
        """analyze a class's members"""

        kinds = {}

        # determine kind
        attrs = sorted(inspect.classify_class_attrs(class_object), key=lambda x: x.name.lower())
        for attr in attrs:
            if attr.name.startswith('__'):
                kind = 'dunders'
            elif attr.kind == 'class method':
                kind = 'methods_class'
            elif attr.kind == 'static method':
                kind = 'methods_static'
            else:
                kind = attr.kind
                if kind != 'data':
                    if kind == 'property':
                        kind = 'properties'
                    else:
                        kind = f'{kind}s'
            if kind != 'dunders' and attr.name.startswith('_'):
                kind += '_private'

            # update kinds dictionary
            if kind in kinds:
                kinds[kind]['members'].update({attr.name: attr.object})
            else:
                kinds.update({kind: {
                    'title': await DocumentationCog.member_kind_title(kind),
                    'members': {attr.name: attr.object}
                }})

        return kinds

    async def analyze_object_members(self, obj: object) -> dict:
        """analyze a non-class object's members"""

        kinds = {}
        members = {k: v for k, v in sorted(inspect.getmembers(obj), key=lambda x: x[0].lower())}

        # separate pygame constants
        if obj in [pygame, pygame_sdl2]:
            kind = 'constants'
            kinds.update({kind: {
                'title': await DocumentationCog.member_kind_title(kind),
                'members': {},
            }})
            for k, v in inspect.getmembers(pygame.constants):
                if not k.startswith('__'):
                    kinds[kind]['members'].update({k: v})
                    members.pop(k, None)

        # all other stuff
        for k, v in members.items():
            if k.startswith('__'):
                kind = 'dunders'
            else:
                private = k.startswith('_')
                if inspect.ismodule(v):
                    if private:
                        kind = 'modules_private'
                    else:
                        kind = 'modules'
                elif inspect.isclass(v):
                    if issubclass(v, BaseException):
                        kind = 'exceptions'
                    elif private:
                        kind = 'classes_private'
                    else:
                        kind = 'classes'
                elif inspect.isroutine(v):
                    if private:
                        kind = 'functions_private'
                    else:
                        kind = 'functions'
                else:
                    if private:
                        kind = 'data_private'
                    else:
                        kind = 'data'
            if kind in kinds:
                kinds[kind]['members'].update({k: v})
            else:
                kinds.update({kind: {
                    'title': await DocumentationCog.member_kind_title(kind),
                    'members': {k: v},
                }})

        return kinds

    async def send_supported_modules(self, ctx: commands.Context) -> None:
        """sends supported modules list to ctx"""

        lines = await self.format_member_kind(self.supported_modules, indent=4)
        pages = await self.paginate_lines(lines)
        await self.send_pages(ctx, pages)

    async def format_member_kinds(
            self,
            members: dict,
            indent: int = 4,
            sep: str = '  ',
            dunders: bool = False,
            data: bool = True,
            private: bool = False,
            constants: bool = False,
    ) -> List[str]:
        """
        input: dict of object's members organized by kind
        output: list of formatted lines

        input dict: {'kind': {'title': 'title string', 'members': []}}
        """

        lines = []

        for kind in await asyncstdlib.sorted(members, key=DocumentationCog.member_kind_sort_order):
            if kind.endswith('_private') and not private:
                continue
            if kind == 'dunders' and not dunders:
                continue
            if kind == 'constants' and not constants:
                continue

            member_kind = await self.format_member_kind(members[kind], indent, sep)
            if lines:
                lines.append('')
            lines.extend(member_kind)

        return lines

    async def format_member_kind(
            self,
            member_kind: dict,
            indent: int,
            sep: str = '  ',
            value: bool = False,
    ) -> List[str]:
        """
        input: dict with object's specific kind of member's title and list of members
        output: list of formatted lines

        input dict: {'title': 'title string', 'members': []}
        """

        # add title and underline
        lines = []
        lines.append(member_kind['title'])
        lines.append('-' * len(member_kind['title']))

        # format member list
        if '\n' in sep:
            for k, v in member_kind['members'].items():
                line = f"{' ' * indent}{k}"
                if value:
                    line += f' = {v}'
                lines.append(line)
        else:
            line = ' ' * indent
            line += sep.join(member_kind['members'])
            lines.append(line)

        return lines

    async def paginate_lines(self, lines: List[str]) -> list:
        """
        paginate lines since discord doesn't let you send
        messages with more than 2000 characters
        """

        if not lines:
            return []
        pages = []
        page = '```'
        while lines:
            line = lines.pop(0)
            if len(page) + len(line) + 1 > 1990:
                pages.append(f'{page}```')
                page = f'```\n{line}'
            else:
                page += f'\n{line}'
        if page:
            pages.append(f'{page}```')

        return pages

    async def send_pages(self, ctx: commands.Context, pages: List[str]) -> None:
        for page in pages:
            await ctx.send(page)

    @commands.command(hidden=True)
    @print_context
    async def this(self, ctx: commands.Context) -> None:
        """send this"""

        msg = '```\n' + codecs.decode(this.s, 'rot13') + '```'
        await ctx.send(msg)


def setup(bot: PythonBot) -> None:
    bot.add_cog(DocumentationCog(bot))
