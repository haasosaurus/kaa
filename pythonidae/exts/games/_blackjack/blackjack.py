# -*- coding: utf-8 -*-


# standard library modules - typing
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union, Tuple, List

# standard library modules
from collections import deque
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

# local modules - game
from .._cards import Card, Deck
from .blackjack_hand import BlackjackHand, BlackjackDealerHand

# local modules - game - phases
from .blackjack_join import BlackjackJoin
from .blackjack_deal import BlackjackDeal
from .blackjack_wager import BlackjackWager
from .blackjack_player import BlackjackPlayer
from .blackjack_dealer import BlackjackDealer
from .blackjack_payout import BlackjackPayout


class Blackjack:
    """overall Blackjack game class"""

    class Phase(enum.Enum):
        """Blackjack round phases"""

        ENTER = enum.auto()
        JOIN = enum.auto()
        WAGER = enum.auto()
        DEAL = enum.auto()
        PLAYER = enum.auto()
        DEALER = enum.auto()
        PAYOUT = enum.auto()
        EXIT = enum.auto()


    def __init__(
        self,
        bot: PythonBot,
        message: discord.Message,
        embed_data: dict,
        emojis: dict,
    ) -> None:
        """initializer"""

        self.bot = bot
        self.message = message
        self.embed_data = embed_data
        self.emojis = emojis

        # game
        self.phase = Blackjack.Phase.ENTER
        self.state = None

        # style
        self.thumbnail_url = 'https://cdn.discordapp.com/attachments/864673127068860476/864767073380597781/blackjack_icon_small_narrow.png'
        self.embed_color = 0xc10000
        self.u200b_ZWSP = '​'  # zero width whitespace
        self.u00a0_NBSP = ' '  # no break space
        self.u2022_bullet = '•'  # bullet
        self.u3000_IS = '　'  # ideographic space

        # dealer
        self.dealer_hand = BlackjackDealerHand()
        self.dealer_blackjack = False
        self.dealer_status = 'In Play'

        # betting
        self.wager_changes_allowed = False
        self.wager_min = 5
        self.wager_max = 20

        # players
        self.players = {}
        self.player_current = None
        self.player_queue = deque()
        self.players_leaving = []
        self.max_player_name_length = 0

        # deck/cards
        self.deck = Deck()
        self.deck.shuffle()

        # game - phases - timeouts
        self.timeout_join = 3
        self.timeout_wager = 3
        self.timeout_deal = 3
        self.timeout_player = 15
        self.timeout_player_busted = 5
        self.timeout_dealer = 15
        self.timeout_payout = 15

        # debug
        self.phase_repetitions = 4


    async def run(self) -> None:
        """start the game"""

        self.phase = Blackjack.Phase.JOIN
        self.state = BlackjackJoin(self, timeout_listener=self.timeout_join)


    async def timeout_handler(self) -> None:
        """timeout handler for all phases"""

        # last completed phase == Phase.ENTER
        if self.phase == Blackjack.Phase.ENTER:
            self.phase = Blackjack.Phase.JOIN


        # last completed phase == Phase.JOIN
        elif self.phase == Blackjack.Phase.JOIN:
            self.phase = Blackjack.Phase.WAGER


        # last completed phase == Phase.WAGER
        elif self.phase == Blackjack.Phase.WAGER:
            self.phase = Blackjack.Phase.DEAL
            # self.phase = Blackjack.Phase.EXIT


        # last completed phase == Phase.DEAL
        elif self.phase == Blackjack.Phase.DEAL:

            # #-------------- DEBUG --------------#
            # while self.phase_repetitions > 0:
            #     self.phase_repetitions -= 1
            #     self.update_credits()
            #     self.cleanup()
            #     self.phase = Blackjack.Phase.WAGER
            #     return self.set_state()

            # self.phase = Blackjack.Phase.EXIT
            # return self.set_state()
            # #------------ END DEBUG ------------#


            if self.dealer_blackjack:

                # resolve round and start a new one
                self.update_credits()
                self.cleanup()
                self.phase = Blackjack.Phase.JOIN

            # otherwise setup player turn queue
            else:

                # make sure queue starts empty
                self.player_queue.clear()

                # add all players who weren't dealt a blackjack
                for player_id, player in self.players.items():
                    if not player['blackjack']:
                        self.player_queue.append(player_id)

                # if there are any players who didn't get blackjack
                if self.player_queue:
                    self.player_current = self.player_queue.popleft()

                    # set phase to PLAYER
                    self.phase = Blackjack.Phase.PLAYER

                # otherwise start a new round
                else:

                    # set phase to WAGER
                    self.phase = Blackjack.Phase.WAGER

        # last completed phase == Phase.PLAYER
        elif self.phase == Blackjack.Phase.PLAYER:

            # if there are still players in the queue
            if self.player_queue:

                # continue in this phase, and set the new current player
                self.player_current = self.player_queue.popleft()

            # otherwise
            else:
                # go to dealer phase
                self.phase = Blackjack.Phase.DEALER

                # debugging Phase.PLAYER
                #self.phase = Blackjack.Phase.EXIT


        # last completed phase == Phase.DEALER
        elif self.phase == Blackjack.Phase.DEALER:

            # go to payout phase
            #self.phase = Blackjack.Phase.PAYOUT

            # debugging Phase.DEALER
            self.phase = Blackjack.Phase.EXIT

        # last completed phase == Phase.PAYOUT
        elif self.phase == Blackjack.Phase.PAYOUT:

            # debugging payout phase
            self.phase = Blackjack.Phase.EXIT


            # # start a new round if there are still players
            # if self.players:

            #     # cleanup players and game state
            #     self.cleanup()

            #     # restart round loop
            #     self.phase = Blackjack.Phase.WAGER

            # # otherwise exit the game
            # else:
            #     self.phase = Blackjack.Phase.EXIT


        # set the next state
        self.set_state()


    def set_state(self):
        if self.phase == Blackjack.Phase.JOIN:
            self.state = BlackjackJoin(
                self,
                timeout_listener=self.timeout_join,
            )

        elif self.phase == Blackjack.Phase.WAGER:
            self.state = BlackjackWager(
                self,
                timeout_listener=None,
                timeout_manual=self.timeout_wager,
            )

        elif self.phase == Blackjack.Phase.DEAL:
            self.state = BlackjackDeal(
                self,
                timeout_listener=self.timeout_deal,
            )

        elif self.phase == Blackjack.Phase.PLAYER:
            self.state = BlackjackPlayer(
                self,
                timeout_listener=self.timeout_player,
                timeout_manual=self.timeout_player_busted,
            )

        elif self.phase == Blackjack.Phase.DEALER:
            self.state = BlackjackDealer(
                self,
                timeout_listener=self.timeout_dealer,
            )

        elif self.phase == Blackjack.Phase.PAYOUT:
            self.state = BlackjackPayout(
                self,
                timeout_listener=self.timeout_payout,
            )

        elif self.phase == Blackjack.Phase.EXIT:
            self.exit()


    def update_credits(self):
        for player in self.players.values():
            player['credits'] += player['difference']


    def cleanup(self):

        # game
        self.wager_changes_allowed = False

        # deck
        self.deck = Deck()
        self.deck.shuffle()

        # dealer
        self.dealer_blackjack = False
        self.dealer_status = 'In Play'
        self.dealer_hand.clear()

        # players
        for player in self.players.values():

            player['hand'].clear()
            player['wager'] = self.wager_min
            player['wager_updated'] = False
            player['blackjack'] = False
            player['difference'] = 0
            player['status'] = 'In Play'



    def exit(self):
        gen = (player for player in self.players if player not in self.players_leaving)
        self.players_leaving.extend(gen)
        while self.players_leaving:
            user_id = self.players_leaving.pop()
            self.player_remove(user_id)


    def player_add(self, user: Union[discord.Member, discord.User]) -> None:
        """add player to the game"""

        if user.id not in self.players:
            self.players[user.id] = {
                'user': user,
                'name': user.display_name,
                'credits': 500,
                'playing': True,
                'avatar_url': user.avatar_url,

                'hand': BlackjackHand(),
                'wager': self.wager_min,
                'wager_updated': False,
                'blackjack': False,
                'difference': 0,
                'status': 'In Play',
            }
            self.bot.blackjack_players[user.id] = self

            # keep track of the longest player name
            length = len(self.players[user.id]['name'])
            if length > self.max_player_name_length:
                self.max_player_name_length = length


    def player_remove(self, user_id) -> None:
        """remove player from the game"""

        self.bot.blackjack_players.pop(user_id, None)
        self.players.pop(user_id, None)


    def player_wager(self, user_id, wager):
        """set a players curent wager and its status"""

        player: dict = self.players.get(user_id)

        # return if they're not a player in this game
        if player is None:
            return

        # return if it's the same wager they already have
        if wager == player['wager']:
            return

        # return if they don't have enough credits
        if wager > player['credits']:
            return

        # return if the wager isn't in the range wager_min, wager_max inclusive
        if wager < self.wager_min or wager > self.wager_max:
            return

        # set their new wager
        player['wager'] = wager
        player['wager_updated'] = True
