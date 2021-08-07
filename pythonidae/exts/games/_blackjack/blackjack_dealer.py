# -*- coding: utf-8 -*-


# standard library modules - typing
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Blackjack
from typing import Union, Tuple, List

# standard library modules
import asyncio
import enum
import itertools
import json
import pathlib
import random

# third-party modules - discord and related
import discord
from discord.ext import commands
import dislash
from dislash import ActionRow, Button, SelectMenu, SelectOption, ButtonStyle

# local modules
from pythonbot import PythonBot

# local modules - game stuff
from .._cards import Card, Deck
from .blackjack_hand import BlackjackHand, BlackjackDealerHand
from .blackjack_state import BlackjackState


class BlackjackDealer(BlackjackState):
    """Blackjack phase state players class"""

    def __init__(self, *args, **kwargs):
        """initializer"""

        super().__init__(*args, **kwargs)

        self.player_hands = ''
        self.player_values = ''

        self.interface_init()
        self.game.bot.loop.create_task(
            self.async_init()
        )


    def interface_init(self):
        self.create_player_fields()
        self.setup_callbacks()


    def create_player_fields(self):

        # aliases
        CARDS = self.game.emojis
        U200B = self.game.u200b_ZWSP
        U3000 = self.game.u3000_IS
        U2022 = self.game.u2022_bullet

        # combinations
        LF = f'\n{U200B}'
        LFLF = f'{U200B}\n{U200B}'
        BULLET_SEP = f'{U3000}{U2022}{U3000}'

        # helper functions
        spacer = lambda n: f'{U200B}{U3000 * n}{U200B}'
        pad_right = lambda n: f'{U3000 * n}{U200B}'
        pad_left = lambda n: f'{U200B}{U3000 * n}'

        # typehints
        card: Card

        max_name_length = 0
        players = []

        # rest of the players
        for player in self.game.players.values():

            player_info = []

            # other_player - name
            player_name = f"{player['name']}:"
            player_info.append(player_name)

            # other_player - name - check against max name length
            if len(player_name) > max_name_length:
                max_name_length = len(player_name)

            # other_player - cards
            player_cards = ''
            for card in player['hand']:
                player_cards += CARDS[card.format_short()]
            player_info.append(player_cards)

            # other_player - value - hard
            player_value_hard = player['hand'].value_hard
            player_info.append(player_value_hard)

            # other_player - value - soft
            player_value_best = player['hand'].value
            player_info.append(player_value_best)

            # other_player - hand status
            status = player['status']
            player_info.append(status)

            # add sublist to main list
            players.append(player_info)

        # create both embed value strings
        for name, cards, value_hard, value_best, status in players:
            self.player_hands += f'`{name:<{max_name_length}}` {cards}\n'
            # self.other_players_values += f'`{U200B}{U3000 * 1}{value_hard:>2}/{value_soft:<2} ({status}){U3000}`\n'
            # self.other_players_values += f'{pad_left(1)}{value_hard}'
            self.player_values += f'{value_hard}'
            if value_hard != value_best:
                self.player_values += f'/{value_best}'
            self.player_values += f'{U3000}({status})\n'

        # added for bottom padding
        self.player_hands += U200B



    async def async_init(self):
        """initializer for async stuff"""

        # edit the message initially
        await self.game.message.edit(embed=self.embed, components=[self.menu_row])


    @property
    def embed(self):
        """main embed for player phase as property"""

        # aliases
        CARDS = self.game.emojis
        U200B = self.game.u200b_ZWSP
        U3000 = self.game.u3000_IS
        U2022 = self.game.u2022_bullet

        # combinations
        LF = f'\n{U200B}'
        LFLF = f'{U200B}\n{U200B}'
        BULLET_SEP = f'{U3000}{U2022}{U3000}'

        # helper functions
        spacer = lambda n: f'{U200B}{U3000 * n}{U200B}'
        pad_right = lambda n: f'{U3000 * n}{U200B}'
        pad_left = lambda n: f'{U200B}{U3000 * n}'

        hand: BlackjackDealerHand = self.game.dealer_hand

        if self.game.dealer_status == 'Busted':
            title_status = ' Busted'
        else:
            title_status = "'s Turn"
        title = f"{U200B}\n**__Kaa (Dealer){title_status}__**{LF}"
        embed = discord.Embed(
            # title=f"**{player['name']}**{LF}",
            title=title,
            color=self.game.embed_color,
        )

        # blackjack title and icon
        embed.set_author(
            name='Blackjack' + pad_right(30),
            icon_url=self.game.thumbnail_url,
        )

        # footer showing current player pic, and the position in queue
        text = (
            f'Phase 5: Dealer Turn{BULLET_SEP}'
            f'Game will continue momentarily'
        )
        embed.set_footer(
            icon_url=self.game.bot.user.avatar_url,
            text=text,
        )


        # dealer cards field
        name = 'Cards'
        value = ''
        card: Card
        for card in hand.iter_all():
            value += CARDS[card.format_short()]
        embed.add_field(name=name, value=value, inline=True)

        # blank field for formatting
        embed.add_field(
            name=U200B,
            value=U200B,
            inline=True,
        )

        name = 'Hard[/Best]'
        # value = f'{pad_left(1)}{hand.value_hard}'
        value = f'{hand.value_hard}'
        if hand.value_hard != hand.value:
            value += f'/{hand.value}'
        if self.game.dealer_status == 'Busted':
            value += ' (Busted)'
        value += LF  # added for bottom padding

        embed.add_field(name=name, value=value, inline=True)




        # players
        name = 'Players'
        value = self.player_hands
        embed.add_field(name=name, value=value, inline=True)

        # blank field for formatting
        embed.add_field(name=U200B, value=U200B, inline=True)

        name = U200B
        value = self.player_values
        embed.add_field(name=name, value=value, inline=True)

        return embed


    def setup_callbacks(self):
        """setup interaction callbacks"""

        # base callbacks
        super().setup_callbacks()
