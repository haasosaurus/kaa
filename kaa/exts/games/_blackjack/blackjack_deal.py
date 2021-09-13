# -*- coding: utf-8 -*-


# standard library modules - typing
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Blackjack
from typing import Union, Tuple, List

# standard library modules
import copy
import enum
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

# local modules - game stuff
from .._cards import Card, Deck
from .blackjack_hand import BlackjackHand
from .blackjack_hand import BlackjackDealerHand
from .blackjack_state import BlackjackState


class BlackjackDeal(BlackjackState):
    """Blackjack phase state join class"""

    def __init__(self, *args, **kwargs):
        """initializer"""

        self.debug_deal = False
        self.debug_dealer_blackjack_hand = BlackjackDealerHand(
            [
                Card(Card.Rank.KING, Card.Suit.SPADES),
                Card(Card.Rank.ACE, Card.Suit.SPADES),
            ]
        )
        self.debug_player_blackjack_hand = BlackjackHand(
            [
                Card(Card.Rank.KING, Card.Suit.SPADES),
                Card(Card.Rank.ACE, Card.Suit.SPADES),
            ]
        )

        super().__init__(*args, **kwargs)

        # players minus dealer blackjack set dealer status loss and show both cards
        self.players_without_blackjack = len(self.game.players)

        self.interface_init()
        self.gameplay_init()
        self.game.bot.loop.create_task(
            self.async_init()
        )

    def gameplay_init(self):
        """gameplay related initializations"""

        self.deal()
        self.resolve_hands()


    def deal(self):

        # dealer
        self.game.dealer_hand.extend(self.game.deck.deal() for _ in range(2))

        # players
        for player in self.game.players.values():
            player['hand'].extend(self.game.deck.deal() for _ in range(2))

        # debug
        if self.debug_deal:
            if self.game.phase_repetitions == 4:
                self.game.dealer_hand = self.debug_dealer_blackjack_hand

            elif self.game.phase_repetitions == 3:
                self.game.dealer_hand = self.debug_dealer_blackjack_hand
                next(iter(self.game.players.values()))['hand'] = self.debug_player_blackjack_hand

            elif self.game.phase_repetitions == 2:
                next(iter(self.game.players.values()))['hand'] = self.debug_player_blackjack_hand


    def resolve_hands(self):

        # dealer has blackjack
        if self.game.dealer_hand.blackjack:
            self.game.dealer_blackjack = True
            self.game.dealer_status = 'Blackjack'

            # check all players
            for player in self.game.players.values():

                # to see if they tie
                if player['hand'].blackjack:
                    player['blackjack'] = True
                    player['difference'] = 0
                    player['status'] = 'Blackjack (Tie)'

                # or if they lose
                else:
                    player['difference'] = player['wager'] * -1
                    player['status'] = 'Loss'

        # dealer doesn't have blackjack
        else:

            # check all players
            for player in self.game.players.values():

                # to see if they immediately win for 3:2 (1.5)
                if player['hand'].blackjack:
                    player['blackjack'] = True
                    player['difference'] = player['wager'] * 1.5
                    player['status'] = 'Blackjack'
                    self.players_without_blackjack -= 1

            # if all players have blackjack
            if not self.players_without_blackjack:

                # and the dealer doesn't
                self.game.dealer_status = 'Loss'



    def interface_init(self):
        """interface related initializations"""

        self.setup_callbacks()


    def setup_callbacks(self):
        """setup interaction callbacks"""

        super().setup_callbacks()


    async def async_init(self):
        """async initializations and actions"""

        # edit the message initially
        await self.game.message.edit(content=None, embed=self.embed, components=[self.menu_row])


    @property
    def embed(self):
        """main embed for join phase as property"""

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


        # create embed with the dict/json template
        d = copy.deepcopy(self.game.embed_data['bj_deal_embed'])
        embed: discord.Embed = discord.Embed.from_dict(d)


        # dealer - col 1 - dealer name/hand
        name = 'Kaa (Dealer)' + pad_right(8)

        # if dealer has blackjack, or all payers have blackjack
        if self.game.dealer_blackjack or not self.players_without_blackjack:

            # show hidden card
            value = CARDS[self.game.dealer_hand.hidden.format_short()]

        # otherwise keep it hidden
        else:
            value = CARDS['card_back']

        # add the remaining dealer cards, should only be one in this phase
        for card in self.game.dealer_hand:
            value += CARDS[card.format_short()]
        value += LF  # add LF for row spacing
        embed.add_field(name=name, value=value, inline=True)

        # dealer - col 2 - status
        name = U200B
        value = self.game.dealer_status
        embed.add_field(name=name, value=value, inline=True)

        # dealer - col 3 - winnings (always none)
        name = U200B
        value = U200B
        embed.add_field(name=name, value=value, inline=True)


        # players
        for player in self.game.players.values():

            # col 1 - player name/hand
            name = player['name']
            value = ''
            card: Card
            for card in player['hand']:
                value += CARDS[card.format_short()]
            value += LF  # add LF for row spacing
            embed.add_field(name=name, value=value, inline=True)

            # col 2 - status
            name = U200B
            value = player['status']
            embed.add_field(name=name, value=value, inline=True)

            # col 3 - winnings/losses
            name = U200B
            diff = player['difference']
            if diff or player['blackjack']:
                value = f'{U200B}{U3000}{diff}'
            else:
                value = U200B
            embed.add_field(name=name, value=value, inline=True)

        # return it
        return embed
