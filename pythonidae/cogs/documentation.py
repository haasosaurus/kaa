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
import inspect
import itertools
import json
import math
import operator
import pathlib
import pprint
import random
import re
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

# discord modules
import discord
from discord.ext import commands


class DocumentationCog(commands.Cog, name="Documentation Commands"):
    """DocumentationCog"""

    def __init__(self, bot):
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
            'inspect': inspect,
            'itertools': itertools,
            'json': json,
            'math': math,
            'operator': operator,
            'pathlib': pathlib,
            'pprint': pprint,
            'random': random,
            're': re,
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
            'pygame': pygame,
        }

    @commands.command(aliases=['docs'])
    async def documentation(
            self,
            ctx,
            module: str = None,
            obj: str = None,
            method: str = None,
    ) -> None:
        """display documentation for a built in function or type"""

        response = ''
        usage = '**`Usage: !docs MODULE TYPE|FUNCTION [METHOD]`**'

        if not module:
            response = (
                usage + '\n\n' + '```Currently available modules:\n\n' +
                '  '.join(sorted(self.modules, key=lambda x: x.lower())) + '```'
            )
            await ctx.send(response)
            return

        if module == 'py':
            module = 'builtins'
        elif module == 'python':
            module = 'builtins'
        elif module == 'np':
            module = 'numpy'
        elif module == 'pd':
            module = 'pandas'

        if module not in self.modules:
            response = (
                f'**`ERROR: MODULE: {module} is unsupported`**\n\n' + usage + '\n\n' +
                '```Currently available modules:\n\n' +
                '  '.join(sorted(self.modules, key=lambda x: x.lower())) + '```'
            )
            await ctx.send(response)
            return

        target_module = self.modules[module]

        if not obj:
            obj_list = [x for x in dir(target_module) if not x.startswith('__')]
            obj_list = sorted(obj_list, key=lambda x: x.lower())
            objs = '  '.join(obj_list)

            response_header = f'**`ERROR: No TYPE|FUNCTION specified for MODULE: {module}`**\n\n'
            response_body = usage + '\n'

            obj_header = '```\nHere is a list of its TYPEs|FUNCTIONs:\n\n'
            obj_body = objs
            obj_footer = '```'

            response = response_header + response_body + obj_header + obj_body + obj_footer

            try:
                await ctx.send(response)
                return
            except discord.HTTPException:
                slices = 2
                while True:
                    index = len(obj_list) // slices
                    if len(' '.join(obj_list)[:index]) < 1800:
                        break
                    slices += 1

                msg = response_header + response_body
                await ctx.send(msg)

                sliced_objs = more_itertools.sliced(obj_list, len(obj_list) // slices)
                for i, sliced_obj in enumerate(sliced_objs):
                    if i == 0:
                        msg = obj_header + ' '.join(sliced_obj) + obj_footer
                    else:
                        msg = '```TYPEs|FUNCTIONs continued:\n\n' + ' '.join(sliced_obj) + obj_footer
                    await ctx.send(msg)
                return

        if obj not in vars(target_module):
            objs = (x for x in dir(target_module) if not x.startswith('__'))
            response = (
                f'**`ERROR: TYPE|FUNCTION: {obj} not found in MODULE {module}`**\n\n' +
                '```Here is a list of its TYPEs|FUNCTIONs:\n\n' +
                '  '.join(sorted(objs, key=lambda x: x.lower())) + '```'
            )
            await ctx.send(response)
            return

        target_obj = vars(target_module)[obj]
        target = None
        target_name = ''

        if method:
            if module == 'pandas' and method in dir(target_obj):
                target = getattr(target_obj, method)
                target_name = method
            elif method in vars(target_obj):
                target = vars(target_obj)[method]
                target_name = method
            else:
                methods = (x for x in dir(target_obj) if not x.startswith('__'))
                response = (
                    f'**`ERROR: METHOD: {method} not found in TYPE|FUNCTION {obj}`**\n\n' +
                    '```Here is a list of its METHODS:\n\n' +
                    '  '.join(sorted(methods, key=lambda x: x.lower())) + '```'
                )
                await ctx.send(response)
                return
        else:
            target = target_obj
            target_name = obj

        if not target:
            response = '**`ERROR: I don\'t have a target even though I should, sorry about that...`**'
            await ctx.send(response)
            return

        response = f'{module}.{obj}'
        method_list = []
        if method:
            response += '.' + method
            methods = ''
        else:
            method_gen = (x for x in dir(target) if not x.startswith('__'))
            method_list = sorted(method_gen, key=lambda x: x.lower())
            if method_list:
                methods = '  '.join(method_list)
            else:
                methods = ''

        try:
            response_body = str(inspect.signature(target)) + '\n    ' + target.__doc__
            response += response_body
        except (ValueError, TypeError):
            response_body = inspect.getdoc(target)
            if response_body:
                if (target_name + '(') not in response_body:
                    response += '(?)'
                response += '\n\n'
                response += response_body
            else:
                response = '```' + response + '```\n**`ERROR: docs not found, sorry...`**'
                await ctx.send(response)
                return

        if methods:
            msg = '```\n' + response + '\n\nMethods:\n    ' + methods + '```'
        else:
            msg = '```\n' + response + '```'
        try:
            await ctx.send(msg)
        except discord.HTTPException:
            if len(response) > 1900:
                response_list = response.strip().split('\n')
                slices = 2
                sliced_strs = None
                while True:
                    sliced_objs = more_itertools.sliced(response_list, len(response_list) // slices)
                    sliced_strs = ['\n'.join(x) for x in sliced_objs]
                    if all(len(x) < 1990 for x in sliced_strs):
                        break
                    slices += 1
                for sliced_str in sliced_strs:
                    if not sliced_str.isspace():
                        msg = '```\n' + sliced_str + '```'
                        await ctx.send(msg)

            if len(methods) < 1990:
                await ctx.send(methods)
            else:
                slices = 2
                sliced_strs = None
                while True:
                    sliced_objs = more_itertools.sliced(method_list, len(method_list) // slices)
                    sliced_strs = ['  '.join(x) for x in sliced_objs]
                    if all(len(x) < 1970 for x in sliced_strs):
                        break
                    slices += 1
                for i, sliced_str in enumerate(sliced_strs):
                    if i == 0:
                        msg = '```\nMethods:\n    ' + sliced_str + '```'
                    else:
                        msg = '```\nMethods continued:\n    ' + sliced_str + '```'
                    await ctx.send(msg)
                return

    async def send_methods(self, method_list):
        pass

    @commands.command(hidden=True)
    async def this(self, ctx):
        msg = '```' + codecs.decode(this.s, 'rot13') + '```'
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(DocumentationCog(bot))


# 2 python processes, one using 32kb memory and another using 34kb memoery
