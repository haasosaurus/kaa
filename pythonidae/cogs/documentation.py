# coding=utf-8


# standard library modules
import argparse
import asyncio
import builtins
import codecs
import collections
import contextlib
import copy
import csv
import datetime
import decimal
import enum
import functools
import gc
import inspect
import itertools
import json
import logging
import math
import netifaces
import numbers
import operator
import pathlib
import pprint
import random
import re
import requests
import scapy.all
import statistics
import string
import this
import time
import timeit
import typing
import types
import weakref

# third-party modules
import more_itertools
import numpy
import pandas
import pygame
import tqdm

# third-party modules - discord
import discord
from discord.ext import commands

# local modules
from utils import print_context


class DocumentationCog(commands.Cog, name='Documentation Commands'):
    """DocumentationCog"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot
        self.modules = {

            # standard library modules
            'argparse': argparse,
            'asyncio': asyncio,
            'builtins': builtins,
            'codecs': codecs,
            'collections': collections,
            'contextlib': contextlib,
            'copy': copy,
            'csv': csv,
            'datetime': datetime,
            'decimal': decimal,
            'enum': enum,
            'functools': functools,
            'gc': gc,
            'inspect': inspect,
            'itertools': itertools,
            'json': json,
            'logging': logging,
            'math': math,
            'netifaces': netifaces,
            'numbers': numbers,
            'operator': operator,
            'pathlib': pathlib,
            'pprint': pprint,
            'random': random,
            're': re,
            'requests': requests,
            'scapy.all': scapy.all,
            'statistics': statistics,
            'string': string,
            'time': time,
            'timeit': timeit,
            'types': types,
            'typing': typing,
            'weakref': weakref,

            # third-party modules
            'more_itertools': more_itertools,
            'numpy': numpy,
            'pandas': pandas,
            'tqdm': tqdm,
            'discord': discord,
            'discord.ext.commands': discord.ext.commands,
        }
        self.standard_module_names = list(self.modules.keys())
        pg_name_checker = lambda x: any((x.startswith('__'), x.isupper(), x.startswith('K_')))
        pg_module_names = [x for x in vars(pygame) if not pg_name_checker(x)]
        pg_modules = {'pygame.' + mdl: getattr(pygame, mdl) for mdl in pg_module_names}
        self.pygame_module_names = ['pygame.' + mdl for mdl in pg_module_names]
        self.modules.update(pg_modules)

    @commands.command(aliases=['docs'])
    @print_context
    async def documentation(
            self,
            ctx: commands.Context,
            module: str = None,
            obj: str = None,
            method: str = None,
    ) -> None:
        """display documentation for a built in function or type"""

        if not module:
            await self.send_members(
                ctx,
                self.standard_module_names,
                title='Currently available modules:'
            )
            await self.send_members(
                ctx,
                self.pygame_module_names,
                title='Pygame modules:'
            )
            await self.send_usage(ctx)
            return

        if module == 'py':
            module = 'builtins'
        elif module == 'python':
            module = 'builtins'
        elif module == 'np':
            module = 'numpy'
        elif module == 'pd':
            module = 'pandas'
        elif module == 'ni':
            module = 'netifaces'
        elif module == 'scapy':
            module = 'scapy.all'

        if module not in self.modules:
            error_msg = f'**`ERROR: MODULE: {module} is unsupported`**'
            await ctx.send(error_msg)
            await self.send_members(
                ctx,
                self.standard_module_names,
                title='Currently available modules:'
            )
            await self.send_members(
                ctx,
                self.pygame_module_names,
                title='Pygame modules:'
            )
            await self.send_usage(ctx)
            return

        target_module = self.modules[module]
        if inspect.isroutine(target_module):
            await self.send_docs_and_methods(ctx, target_module, module)
            return

        if not obj:
            # error_msg = f'**`ERROR: No member specified for {module}`**'
            obj_list_header = f"**`{module}'s TYPEs|FUNCTIONs:`**"
            obj_list = await self.make_members_list(target_module, module)
            # await ctx.send(error_msg)
            await ctx.send(obj_list_header)
            if module == 'scapy.all':
                await ctx.send('**`scapy stuff too long to list`**')
            else:
                await self.send_members(ctx, obj_list)
            await self.send_usage(ctx)
            return

        if obj not in dir(target_module):
            error_msg = f'**`ERROR: {obj} not found in {module}`**'
            obj_list_header = f"**`{module}'s TYPEs|FUNCTIONs:`**"
            obj_list = await self.make_members_list(target_module, module)
            await ctx.send(error_msg)
            await ctx.send(obj_list_header)
            if module == 'scapy.all':
                await ctx.send('**`scapy stuff too long to list`**')
            else:
                await self.send_members(ctx, obj_list)
            await self.send_usage(ctx)
            return

        target_obj = getattr(target_module, obj)
        target = None
        target_name = ''

        if method and method not in dir(target_obj):
            error_msg = f'**`ERROR: {method} not found in {obj}`**'
            obj_list_header = f"**`{obj}'s METHODs:`**"
            obj_list = await self.make_members_list(target_obj, obj)
            await ctx.send(error_msg)
            await ctx.send(obj_list_header)
            await self.send_members(ctx, obj_list, title='Methods:')
            await self.send_usage(ctx)
            return

        if method:
            target = getattr(target_obj, method)
            target_name = method
        else:
            target = target_obj
            target_name = obj

        if not target:
            error_msg = '**`ERROR: failed to acquire target, sorry about that`**'
            await ctx.send(error_msg)
            return

        await self.send_docs_and_methods(ctx, target, target_name, obj, method)

    async def send_docs_and_methods(
            self,
            ctx: commands.Context,
            target,
            target_name: str,
            obj=None,
            method=None
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

    async def send_usage(self, ctx: commands.Context) -> None:
        """send usage information"""

        usage = '**`Usage: !docs MODULE TYPE|FUNCTION [METHOD]`**'
        await ctx.send(usage)

    @commands.command(hidden=True)
    @print_context
    async def this(self, ctx: commands.Context) -> None:
        """send this"""

        msg = '```\n' + codecs.decode(this.s, 'rot13') + '```'
        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DocumentationCog(bot))
