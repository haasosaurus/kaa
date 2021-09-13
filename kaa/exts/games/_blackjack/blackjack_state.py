# -*- coding: utf-8 -*-


# standard library modules - typing
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Blackjack
from typing import Union, Tuple, List

# standard library modules
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
from exts.games._cards import Card, Deck



class BlackjackState:
    """Blackjack phase state base class"""

    def __init__(self, game: Blackjack, timeout_listener=30, timeout_manual=None):
        """initializer"""

        # debugging
        self.debug = True

        # parent game object
        self.game = game

        # timeouts
        self.timeout_listener = timeout_listener
        self.timeout_manual = timeout_manual

        # univeral embeds and components
        self.rules_embed = discord.Embed.from_dict(self.game.embed_data['bj_rules_embed'])
        self.menu_row = dislash.ActionRow.from_dict(self.game.embed_data['bj_menu_row'])

        # set gameplay message and create listener on it
        self.listener: dislash.ClickListener = self.game.message.create_click_listener(timeout=self.timeout_listener)


    def setup_callbacks(self, join_phase=False):
        """setup interaction callbacks"""

        # timeout callback
        self.listener.timeout(self.game.timeout_handler)

        # button callback - rules
        self.button_rules_handler = self.listener.matching_id(
            'button_bj_rules',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_rules_handler)

        # button callbacks - only if the state is not the join state
        if not join_phase:

            # button callback - join
            self.button_join_handler = self.listener.matching_id(
                'button_bj_join',
                cancel_others=True,
                reset_timeout=True,
            )(self.button_join_handler)

            # button callback - leave
            self.button_leave_handler = self.listener.matching_id(
                'button_bj_leave',
                cancel_others=True,
                reset_timeout=True,
            )(self.button_leave_handler)


    async def button_join_handler(self, inter: dislash.MessageInteraction):
        """handle join button clicks"""

        await inter.reply('joining here will be implemented', ephemeral=True)


    async def button_rules_handler(self, inter: dislash.MessageInteraction):
        """handle rules button clicks"""

        # send rules as a hidden message
        await inter.reply(
            embed=self.rules_embed,
            ephemeral=True,
        )


    async def button_leave_handler(self, inter: dislash.MessageInteraction):
        """handle leave button clicks"""

        await inter.reply('leaving here will be implemented', ephemeral=True)
