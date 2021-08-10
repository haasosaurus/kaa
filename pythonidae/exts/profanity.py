# -*- coding: utf-8 -*-


# standard library modules
import itertools
import json
import pathlib
import re
from typing import List, Union

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Profanity(commands.Cog, name='profanity'):
    def __init__(self, bot: PythonBot) -> None:
        self.bot = bot

        self.subs = {}
        self.build_subs()

        # create pattern
        start = r"(^|\s)"
        end = r"(?=$|\s)"
        punct = (
            r"([\)\$\+\=\:\|\]\\\-\*\!\(\^\[\}\{\<\>\?\.%,`@#/~&_;'"
            r'\"]*?)'
        )
        pattern = f"{start}{punct}({'|'.join(self.subs)}){punct}{end}"

        # compile pattern
        self.sub_regex = re.compile(
            pattern=pattern,
            flags=re.MULTILINE | re.IGNORECASE,
        )

    def build_subs(self):

        # keys as lists for multi-character alts in the future
        alts = {}

        # load alts dict from json
        conversion_json_path = 'resources/data/alt_chars.json'
        with pathlib.Path(conversion_json_path).open() as f:
            alts = json.load(f)

        # load translation dict from json
        conversion_json_path = 'resources/data/profanity_substitutions.json'
        with pathlib.Path(conversion_json_path).open() as f:
            self.subs = json.load(f)

        # generate alternate spellings
        for word in list(self.subs):
            sub = self.subs[word]
            expanded = [alts[letter] for letter in word]
            for variant in itertools.product(*expanded):
                variant = ''.join(variant)
                self.subs[variant] = sub

    def translate(self, m: re.Match):
        return '{0}{1}{3}{2}'.format(*m.group(1, 2, 4), self.subs[m.group(3)])


    @commands.Cog.listener(name='on_message')
    async def profanity_translator(self, message: discord.Message) -> None:
        """
        deletes messages with profanity, replaces with edited message as webhook
        """

        # return if it's a dm
        if not message.guild:
            return

        # DEBUG: return if not on the test server
        if message.guild.id != 864816273618763797:
            return

        # return if it's a webhook/bot
        if message.webhook_id or message.author.bot:
            return

        # create translated str
        translated = re.sub(
            pattern=self.sub_regex,
            repl=self.translate,
            string=message.content,
            count=0,
        )

        # if it's not the same as the original message
        if translated != message.content:

            # delete the original message
            await message.delete()

            # make the webhook creation and deletion into a context manager maybe
            webhook: discord.Webhook = await message.channel.create_webhook(
                name=message.author.display_name
            )

            # send the webhook
            await webhook.send(
                translated,
                avatar_url=message.author.avatar_url
            )

            # delete the webhook
            await webhook.delete()


def setup(bot: PythonBot) -> None:
    bot.add_cog(Profanity(bot))
