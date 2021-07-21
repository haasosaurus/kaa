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
from pythonbot import PythonBot

# local modules - game stuff
from .._cards import Card, Deck
from .blackjack_state import BlackjackState
from .blackjack_hand import BlackjackHand


class BlackjackJoin(BlackjackState):
    """Blackjack phase state join class"""

    def __init__(self, *args, **kwargs):
        """initializer"""

        super().__init__(*args, **kwargs)
        self.interface_init()
        self.game.bot.loop.create_task(
            self.async_init()
        )


    def interface_init(self):
        """interface related initializatoins"""

        self.setup_callbacks()


    def setup_callbacks(self):
        """setup interaction callbacks"""

        # base callbacks
        super().setup_callbacks(join_phase=True)

        # button callback - join - join state specific variant
        self.button_join_handler = self.listener.matching_id(
            'button_bj_join',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_join_handler)

        # button callback - leave - join state specific variant
        self.button_leave_handler = self.listener.matching_id(
            'button_bj_leave',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_leave_handler)


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
        d = copy.deepcopy(self.game.embed_data['bj_join_embed'])
        embed: discord.Embed = discord.Embed.from_dict(d)

        # footer with current round phase
        text = f'Phase 0: Join{BULLET_SEP}(Game will continue in {self.timeout_listener} seconds)'
        embed.set_footer(
            icon_url=self.game.bot.user.avatar_url,
            text=text,
        )

        # players/credits row
        name = U200B
        player_names = ''
        player_credits = ''
        if self.game.players:
            for player in self.game.players.values():
                player_names += f"**{player['name']}**\n"
                player_credits += f"{player['credits']}\n"

        else:
            player_names = 'None\n'
        player_names += U200B  # adding for padding
        embed.add_field(name=name, value=player_names, inline=True)

        embed.add_field(name=U200B, value=U200B, inline=True)

        name = '**__Credits__**'
        embed.add_field(name=name, value=player_credits, inline=True)

        return embed



    async def button_join_handler(self, inter: dislash.MessageInteraction):
        """handle join button clicks"""

        # return if the button clicker is already playing
        if inter.author.id in self.game.players:
            return await inter.reply("You're already in the game", ephemeral=True)

        # retrieve the user
        user: discord.User = await self.game.bot.fetch_user(inter.author.id)

        # add player to the game
        self.game.player_add(user)

        # defer reply and edit the game message
        await inter.reply(type=dislash.ResponseType.DeferredUpdateMessage)
        await inter.message.edit(embed=self.embed)


    async def button_leave_handler(self, inter: dislash.MessageInteraction):
        """handle leave button clicks"""

        # return if the button clicker isn't already playing
        if inter.author.id not in self.game.players:
            return await inter.reply("You're not in the game", ephemeral=True)

        # remove the clicker from the players dict
        if self.game.players.pop(inter.author.id, None) is not None:

            # defer reply and edit the game message
            await inter.reply(type=dislash.ResponseType.DeferredUpdateMessage)
            await inter.message.edit(embed=self.embed)
