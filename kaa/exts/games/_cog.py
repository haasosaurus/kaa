# -*- coding: utf-8 -*-


# standard library modules - typing
from typing import Union, Tuple, List

# standard library modules
import asyncio
import json
import pathlib
import random

# third-party modules - discord and related
import discord
from discord.ext import commands
import dislash
from dislash import ActionRow, Button, SelectMenu, SelectOption, ButtonStyle

# local modules
from kaa import Kaa
from utils import print_context
from ._blackjack import Blackjack


class Games(commands.Cog, name='games'):
    """
    game commands
    """

    def __init__(self, bot: Kaa) -> None:
        """initializer"""

        self.bot = bot

        # debugging
        self.debug = True

        # embed formatting/styling
        self.u200b_ZWSP = '​'  # zero width whitespace
        self.u00a0_NBSP = ' '  # no break space
        self.u2022_bullet = '•'  # bullet
        self.u3000_IS = '　'  # ideographic space
        self.bj_embed_color = 0xc10000  # same red as card emojis
        self.blackjack_thumbnail_url = (
            'https://cdn.discordapp.com/attachments/864673127068860476/864767073380597781/blackjack_icon_small_narrow.png'
        )

        # custom emojis
        self.card_emojis_json_path = 'resources/data/card_emojis.json'
        self.card_emojis = None
        self.load_emoji_json_data()

        # embed data
        self.embed_names_and_paths = (
            # static
            ('bj_rules_embed', 'resources/data/game_embeds/bj_rules_embed.json'),
            ('bj_menu_row', 'resources/data/game_embeds/bj_menu_row.json'),

            # join
            ('bj_join_embed', 'resources/data/game_embeds/bj_join_embed.json'),

            # wager
            ('bj_wager_embed', 'resources/data/game_embeds/bj_wager_embed.json'),
            ('bj_wager_row', 'resources/data/game_embeds/bj_wager_row.json'),

            # deal
            ('bj_deal_embed', 'resources/data/game_embeds/bj_deal_embed.json'),

            # player
            ('bj_player_embed', 'resources/data/game_embeds/bj_player_embed.json'),
            ('bj_player_row', 'resources/data/game_embeds/bj_player_row.json'),

            # dealer
            ('bj_dealer_embed', 'resources/data/game_embeds/bj_dealer_embed.json'),

            # payout
        )
        self.embed_data = {}

        self.load_embed_json_data()

        self.bot.blackjack_players = {}


    @commands.command(
        name='blackjack_wager',
        aliases=['bj_wager', 'blackjack_bet', 'bj_bet', 'bet'],
        description='make wager in blackjack',
        help='make wager in blackjack',
    )
    @print_context
    async def blackjack_wager_command(self, ctx: commands.Context, wager: int) -> None:
        """
        make wager in blackjack
        """

        # delete message to reduce spam
        message: discord.Message = ctx.message
        await message.delete()

        # try to get game instance, return on fail
        game: Blackjack = self.bot.blackjack_players.get(ctx.author.id, None)
        if game is None:
            return

        # if the game is accepting wager changes
        if game.wager_changes_allowed:

            # set player wager
            game.player_wager(ctx.author.id, wager)


    @commands.command(
        name='blackjack',
        aliases=['bj'],
        description='start a blackjack game',
        help='start a multiplayer blackjack game',
    )
    @commands.is_owner()
    @print_context
    async def blackjack_command(self, ctx: commands.Context):
        """
        start a multiplayer blackjack game
        """

        # must add player id to set on cog level and force them to play only one game at once
        # need to implement that thing where it can make sure their id is removed when the command exits

        msg = await ctx.send('blackjack')
        game = Blackjack(
            bot=self.bot,
            message=msg,
            embed_data=self.embed_data,
            emojis=self.card_emojis,
        )
        game.player_add(ctx.author)
        await game.run()


    def load_embed_json_data(self):

        for name, path in self.embed_names_and_paths:
            p = pathlib.Path(path)

            if not p.exists():
                print(f"Error: '{p}' does not exist")
                continue

            with p.open('r') as f:
                d = json.load(f)
                self.embed_data[name] = d


    def load_emoji_json_data(self):
        """load custom emoji strings into the dict"""

        path = pathlib.Path(self.card_emojis_json_path)
        if not path.exists():
            print(f"Error: '{path}' does not exist")
            return

        with path.open('r') as f:
            d = json.load(f)
            self.card_emojis = d


    @commands.command(
        name='dice',
        aliases=['roll'],
        description='roll the dice',
        help='roll between 1 and 100 dice with between 2 and 1000 sides',
    )
    @print_context
    async def dice_command(
            self,
            ctx: commands.Context,
            amount: int = None,
            sides: int = None,
    ) -> None:
        """
        roll between 1 and 100 dice with between 2 and 1000 sides
        """

        amount = amount if amount else 1
        sides = sides if sides else 6
        if (0 < amount <= 100) and (1 < sides <= 1000):
            msg = ', '.join(str(random.randint(1, sides)) for _ in range(amount))
            await self.bot.send_info_msg(ctx, msg)
        else:
            msg = 'ranges are: 0 < AMOUNT <= 100, 1 < SIDES <= 1000'
            await self.bot.send_error_msg(ctx, msg)


    @commands.command(
        name='coin',
        aliases=['flip'],
        description='flip a coin',
        help='flip a coin',
    )
    @print_context
    async def coin_command(self, ctx: commands.Context) -> None:
        """
        flip a coin
        """

        msg = random.choice(['heads', 'tails'])
        await self.bot.send_info_msg(ctx, msg)
