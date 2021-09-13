# -*- coding: utf-8 -*-


# standard library modules
import itertools
import json
import pathlib
import re
from typing import List, Union

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from kaa import Kaa
from utils import print_context


class Profanity(commands.Cog, name='profanity'):
    """
    translates profanity to less offensive things
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

        # style and formatting
        self.embed_color = 0xfed142

        # extention specific stuff
        self.subs = {}
        self.regex_soft = None
        self.regexes_hard = []
        self.build_subs_and_regexes()

    def build_subs_and_regexes(self):
        """
        builds word substitution dict and regexes to use with it
        """

        # keys as lists for multi-character alts in the future
        alt_chars = {}

        # load alts dict from json
        conversion_json_path = 'resources/data/alt_chars.json'
        with pathlib.Path(conversion_json_path).open() as f:
            alt_chars = json.load(f)

        # load soft translation dict from json
        conversion_json_path = 'resources/data/profanity_subs_soft.json'
        with pathlib.Path(conversion_json_path).open() as f:
            subs_soft = json.load(f)

        # generate alternate spellings
        self.create_variants(subs_soft, alt_chars)

        # create pattern
        start = r'''(^|\W)('''
        end = r''')(?=$|\W)'''
        pattern = f"{start}{'|'.join(subs_soft)}{end}"

        # compile pattern
        self.regex_soft = re.compile(
            pattern=pattern,
            flags=re.MULTILINE | re.IGNORECASE,
        )

        # update main subs dict
        self.subs.update(subs_soft)

        # now do the hard subs
        conversion_json_path = 'resources/data/profanity_subs_hard.json'
        with pathlib.Path(conversion_json_path).open() as f:
            hard_rounds = json.load(f)

        # do all three rounds
        for round in ('round1', 'round2', 'round3'):
            subs_hard = hard_rounds[round]

            # generate alternate spellings
            self.create_variants(subs_hard, alt_chars)

            # compile pattern
            pattern = f"({'|'.join(subs_hard)})"
            regex = re.compile(
                pattern=pattern,
                flags=re.MULTILINE | re.IGNORECASE,
            )
            self.regexes_hard.append(regex)

            # update main subs dict
            self.subs.update(subs_hard)

    def create_variants(self, subs: dict, alt_chars: dict) -> None:
        """
        creates word variants for a given substitution dict using alt chars dict
        """

        for word in list(subs):
            sub = subs[word]
            expanded = [alt_chars[letter] for letter in word]
            for variant in itertools.product(*expanded):
                variant = ''.join(variant)
                subs[variant] = sub

    def translate_soft(self, m: re.Match):
        return m.group(1) + self.subs[m.group(2).lower()]

    def translate_hard(self, m: re.Match) -> str:
        return self.subs[m.group(1).lower()]

    async def run_regex(self, regex: re.Pattern, translator, text: str) -> str:
        return re.sub(
            pattern=regex,
            repl=translator,
            string=text,
            count=0,
        )

    @commands.Cog.listener(name='on_message')
    async def profanity_translator(self, message: discord.Message) -> None:
        """
        listens for messages with profanity if one is detected it deletes it and
        replaces with edited message as webhook masquerading as the user
        """

        # return if it's a dm
        if not message.guild:
            return

        # return if it's not in one of the test channels
        test_channels = {
            875283005130801172,  # sfw-zone
            864922816344358982,  # spam
        }
        if message.channel.id not in test_channels:
            return

        # return if it's a webhook/bot
        if message.webhook_id or message.author.bot:
            return

        # do hard sub translations
        translated = message.content
        for regex in self.regexes_hard:
            translated = await self.run_regex(regex, self.translate_hard, translated)


        # do soft sub translation
        translated = await self.run_regex(self.regex_soft, self.translate_soft, translated)

        # if it's not the same as the original message
        if translated != message.content:

            # delete the original message
            await message.delete()

            embed = discord.Embed(
                description=translated,
                color=self.embed_color,
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )
            await message.channel.send(embed=embed)

            # # make the webhook creation and deletion into a context manager maybe
            # webhook: discord.Webhook = await message.channel.create_webhook(
            #     name=message.author.display_name
            # )

            # # send the webhook
            # await webhook.send(
            #     translated,
            #     avatar_url=message.author.avatar_url,
            #     wait=True,
            # )

            # # delete the webhook
            # await webhook.delete()


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    bot.add_cog(Profanity(bot))
