# -*- coding: utf-8 -*-


# standard library modules - typing
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Blackjack
from typing import Union, Tuple, List

# standard library modules
import asyncio
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
from .blackjack_state import BlackjackState


class BlackjackWager(BlackjackState):
    """Blackjack phase state join class"""

    def __init__(self, *args, **kwargs):
        """initializer"""

        super().__init__(*args, **kwargs)
        self.bj_wager_row = None
        self.interface_init()
        self.gameplay_init()
        self.game.bot.loop.create_task(
            self.async_init()
        )


    def interface_init(self):
        """interface related initializations"""

        self.bj_wager_row = ActionRow.from_dict(self.game.embed_data['bj_wager_row'])
        self.setup_callbacks()


    def setup_callbacks(self):
        """setup interaction callbacks"""

        super().setup_callbacks()

        # button callback - done
        self.button_done_handler = self.listener.matching_id(
            'button_bj_done',
            cancel_others=True,
            reset_timeout=True,
        )(self.button_done_handler)


    def gameplay_init(self):
        """gameplay related initializaiton"""

        self.waiting_on = set()


    async def async_init(self):
        """async initializations and actions"""

        # edit the message initially
        await self.game.message.edit(content=None, embed=self.embed, components=[self.bj_wager_row, self.menu_row])
        await self.wager_loop()


    async def wager_loop(self):
        """check for wager updates every 0.5 seconds for self.timeout_manual seconds"""

        # add all players to check later if everyone has finished betting
        self.waiting_on.update(self.game.players)

        # set game to allow wager changes
        self.game.wager_changes_allowed = True

        # check if any player has updated their wager
        for _ in range((self.timeout_manual - 1) * 2):

            # if everyone has finished
            if not self.waiting_on:
                break

            # otherwise wait half a second
            await asyncio.sleep(0.5)

            # check if any player has updated their wager
            players = iter(self.game.players.values())
            for player in players:
                if player['wager_updated']:
                    player['wager_updated'] = False

                    # set wager_updated to false for remaining players and expend iterator
                    for player in players:
                        player['wager_updated'] = False

                    # edit the embed to show the updated wagers
                    await self.game.message.edit(embed=self.embed)

        # set game to disallow wager changes
        self.game.wager_changes_allowed = False

        # wait a second to let players view the final wagers
        await asyncio.sleep(1)

        # kill the listener and run the game's timeout handler
        self.listener.kill()
        return await self.game.timeout_handler()


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


        # create a new embed
        embed = discord.Embed(
            description=(
                'Use the !bet <amount> command to bet, '
                f'min: {self.game.wager_min}, max: {self.game.wager_max}{LF}'
            ),
            color=self.game.embed_color,
        )

        # blackjack title and icon
        embed.set_author(
            name='Blackjack' + pad_right(30),
            icon_url=self.game.thumbnail_url,
        )

        # footer with current round phase
        text = (
            f'Phase 1: Wager{BULLET_SEP}'
            f'(Game will continue in {self.timeout_manual} seconds)'
        )
        embed.set_footer(
            icon_url=self.game.bot.user.avatar_url,
            text=text,
        )


        # data for player name/credits/wager
        player_names = ''
        player_credits = ''
        player_wagers = ''
        if self.game.players:
            for player in self.game.players.values():
                player_names += f"**{player['name']}**\n"
                player_credits += f"{player['credits']}\n"
                player_wagers += f"{player['wager']}\n"
        else:
            player_names = 'None\n'
            player_credits = U200B
            player_wagers = U200B
        player_names += U200B  # adding for padding

        # row 1 - col 1 - header - blank for formatting
        # embed.add_field(name=U200B, value=player_names, inline=True)
        embed.add_field(name=spacer(14), value=player_names, inline=True)

        # row 1 - col 2 - header - credits
        name = '**__Credits__**'
        embed.add_field(name=name, value=player_credits, inline=True)

        # row 1 - col 3 - header - wagers
        name = '**__Wager__**'
        embed.add_field(name=name, value=player_wagers, inline=True)


        return embed


    async def button_done_handler(self, inter: dislash.MessageInteraction):
        """handle leave button clicks"""

        # remove player from set of players who haven't finished placing a wager
        if inter.author.id in self.waiting_on:
            self.waiting_on.remove(inter.author.id)

            # defer reply
            await inter.reply(type=dislash.ResponseType.DeferredUpdateMessage)
