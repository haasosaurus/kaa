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
from .blackjack_hand import BlackjackHand
from .blackjack_state import BlackjackState


class BlackjackPlayer(BlackjackState):
    """Blackjack phase state players class"""

    def __init__(self, *args, **kwargs):
        """initializer"""

        super().__init__(*args, **kwargs)

        self.other_players_hands = ''
        self.other_players_values = ''
        self.player_position = 1
        self.action_taken = False
        self.row1 = None

        self.interface_init()
        self.game.bot.loop.create_task(
            self.async_init()
        )


    def interface_init(self):
        self.row1 = ActionRow.from_dict(self.game.embed_data['bj_player_row1'])
        self.create_other_players_fields()
        self.setup_callbacks()


    def create_other_players_fields(self):

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
        other_players = []

        # rest of the players
        for i, (player_id, player) in enumerate(self.game.players.items(), 1):
            if player_id == self.game.player_current:
                self.player_position = i
                continue

            other_player = []

            # other_player - name
            player_name = f"{player['name']}:"
            other_player.append(player_name)

            # other_player - name - check against max name length
            if len(player_name) > max_name_length:
                max_name_length = len(player_name)

            # other_player - cards
            player_cards = ''
            for card in player['hand']:
                player_cards += CARDS[card.format_short()]
            other_player.append(player_cards)

            # other_player - value - hard
            player_value_hard = player['hand'].value_hard
            other_player.append(player_value_hard)

            # other_player - value - soft
            player_value_best = player['hand'].value
            other_player.append(player_value_best)

            # other_player - hand status
            status = player['status']
            other_player.append(status)

            # add sublist to main list
            other_players.append(other_player)

        # create both embed value strings
        for name, cards, value_hard, value_best, status in other_players:
            self.other_players_hands += f'`{name:<{max_name_length}}` {cards}\n'
            # self.other_players_values += f'`{U200B}{U3000 * 1}{value_hard:>2}/{value_soft:<2} ({status}){U3000}`\n'
            # self.other_players_values += f'{pad_left(1)}{value_hard}'
            self.other_players_values += f'{value_hard}'
            if value_hard != value_best:
                self.other_players_values += f'/{value_best}'
            self.other_players_values += f'{U3000}({status})\n'

        # added for bottom padding
        self.other_players_hands += U200B



    async def async_init(self):
        """initializer for async stuff"""

        # edit the message initially
        await self.game.message.edit(embed=self.embed, components=[self.row1, self.menu_row])


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

        player: dict = self.game.players[self.game.player_current]
        hand: BlackjackHand = player['hand']

        if player['status'] = 'Busted':
            title_status = ' Busted'
        else:
            title_status = "'s Turn"
        title = f"{U200B}\n**__{player['name']}{title_status}__**{LF}"
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
            f'Phase 4: Player Turns{BULLET_SEP}'
            f'Player {self.player_position} of out {len(self.game.players)}'
        )
        embed.set_footer(
            icon_url=player['avatar_url'],
            text=text,
        )


        # # wager and chips fields
        wager = player['wager']
        remaining = player['credits'] - wager

        name = 'Wager'
        value = f'{wager} credits'
        embed.add_field(name=name, value=value, inline=True)

        # blank field with extra line for bottom padding
        embed.add_field(name=U200B, value=LFLF, inline=True)

        name = 'Remaining'
        value = f'{remaining} credits'
        embed.add_field(name=name, value=value, inline=True)






        # player cards field
        # name = f"{player['name']}{pad_right(11)}"
        # name = f"{player['name']}"
        name = 'Cards'
        value = ''
        card: Card
        for card in hand:
            value += CARDS[card.format_short()]
        embed.add_field(name=name, value=value, inline=True)

        # blank field for formatting
        embed.add_field(
            name=U200B,
            value=U200B,
            inline=True,
        )

        name = 'Hard/Best'
        # value = f'{pad_left(1)}{hand.value_hard}'
        value = f'{hand.value_hard}'
        if hand.value_hard != hand.value:
            value += f'/{hand.value}'
        if player['status'] == 'Busted':
            value += ' (Busted)'
        value += LF  # added for bottom padding

        embed.add_field(name=name, value=value, inline=True)







        # dealer - name
        dealer_name = 'Kaa (Dealer)'

        # dealer - cards
        dealer_cards = CARDS['card_back']
        for card in self.game.dealer_hand:
            dealer_cards += CARDS[card.format_short()]

        # dealer - value - hard
        dealer_value_hard = self.game.dealer_hand.value_hard

        # dealer - value - soft
        dealer_value_best = self.game.dealer_hand.value_hidden


        # player cards field
        name = dealer_name
        # value = ''
        # for card in dealer_cards:
            # value += CARDS[card.format_short()]
        embed.add_field(name=name, value=dealer_cards, inline=True)

        # blank field for formatting
        embed.add_field(
            name=U200B,
            value=U200B,
            inline=True,
        )

        # name = '(Shown)'
        name = U200B
        value = f'{dealer_value_hard}'
        if dealer_value_hard != dealer_value_best:
            value += f'/{dealer_value_best}'

        # add an extra blank newline at the bottom for formatting
        value += LF

        embed.add_field(name=name, value=value, inline=True)











        if len(self.game.players) > 1:

            #other game participants, starting with the dealer
            name = 'Other Players'
            value = self.other_players_hands
            embed.add_field(name=name, value=value, inline=True)

            # blank field for formatting
            embed.add_field(name=U200B, value=U200B, inline=True)

            name = U200B
            value = self.other_players_values
            embed.add_field(name=name, value=value, inline=True)

        return embed


    def setup_callbacks(self):
        """setup interaction callbacks"""

        # base callbacks
        super().setup_callbacks()

        # button callbacks - stand
        self.button_stand_handler = self.listener.matching_id(
            'button_bj_stand',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_stand_handler)

        # button callbacks - hit
        self.button_hit_handler = self.listener.matching_id(
            'button_bj_hit',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_hit_handler)

        # button callbacks - double down
        self.button_double_down_handler = self.listener.matching_id(
            'button_bj_double_down',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_double_down_handler)

        # button callbacks - surrender
        self.button_surrender_handler = self.listener.matching_id(
            'button_bj_surrender',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_surrender_handler)


    async def button_stand_handler(self, inter: dislash.MessageInteraction):
        """handle stand button clicks"""

        # incorrect player clicks
        if inter.author.id != self.game.player_current:
            msg = "It's not your turn"
            return await inter.reply(content=msg, ephemeral=True)

        # correct player clicks, gracefully end player turn
        self.row1.disable_buttons()
        self.listener.kill()
        await asyncio.sleep(self.timeout_manual)
        await self.game.timeout_handler()


    async def button_hit_handler(self, inter: dislash.MessageInteraction):
        """handle hit button clicks"""

        # incorrect player clicks
        if inter.author.id != self.game.player_current:
            msg = "It's not your turn"
            return await inter.reply(content=msg, ephemeral=True)

        # correct player clicks
        self.row1.disable_buttons(2, 3)
        player = self.game.players[self.game.player_current]
        hand: BlackjackHand = player['hand']
        deck = self.game.deck
        hand.append(deck.deal())
        if hand.value > 21:
            player['status'] = 'Busted'
            self.row1.disable_buttons(0, 1)

        # handle interaction and update the embed to show player busted
        await inter.reply(type=dislash.ResponseType.DeferredUpdateMessage)
        await inter.message.edit(embed=self.embed, components=[self.row1, self.menu_row])

        # gracefully end player turn
        self.listener.kill()
        await asyncio.sleep(self.timeout_manual)
        await self.game.timeout_handler()


    async def button_double_down_handler(self, inter: dislash.MessageInteraction):
        """handle double down button clicks"""

        # incorrect player clicks
        if inter.author.id != self.game.player_current:
            msg = "It's not your turn"
            return await inter.reply(content=msg, ephemeral=True)

        # correct player clicks
        pass


    async def button_surrender_handler(self, inter: dislash.MessageInteraction):
        """handle surrender button clicks"""

        # incorrect player clicks
        if inter.author.id != self.game.player_current:
            msg = "It's not your turn"
            return await inter.reply(content=msg, ephemeral=True)

        # correct player clicks
        pass
