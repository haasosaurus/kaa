from reactionmenu import ButtonsMenu
from reactionmenu.abc import _PageController

import asyncio
import collections
import inspect

from reactionmenu.errors import *
from reactionmenu.decorators import ensure_not_primed

import discord
from dislash import ActionRow


class BetterMenu(ButtonsMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ensure_not_primed
    async def start(self, start_index=0):

        # allow menu to start on a page other than 0
        if start_index < 0 or start_index >= len(self._ButtonsMenu__pages):
            start_index = 0

        # before the menu starts, ensure the "components" kwarg is implemented inside the `_ctx.send` method. If it's missing, raise an error (the menu cannot function without it)
        send_info = inspect.getfullargspec(self._ctx.send)
        if 'components' not in send_info.kwonlyargs:
            raise MissingSetting('The "components" kwarg is missing from the .send() method. Did you forget to initialize the menu first using static method ButtonsMenu.initialize(...)?')

        # ensure at least 1 page exists before starting the menu
        if self._menu_type in (ButtonsMenu.TypeEmbed, ButtonsMenu.TypeText) and not self._ButtonsMenu__pages:
            raise NoPages("You cannot start a ButtonsMenu when you haven't added any pages")

        # ensure only valid menu types have been set
        if self._menu_type not in (ButtonsMenu.TypeEmbed, ButtonsMenu.TypeEmbedDynamic, ButtonsMenu.TypeText):
            raise ButtonsMenuException('ButtonsMenu menu_type not recognized')

        # add page (normal menu)
        if self._menu_type == ButtonsMenu.TypeEmbed:
            self._refresh_page_director_info(ButtonsMenu.TypeEmbed, self._ButtonsMenu__pages)
            self._msg = await self._ctx.send(embed=self._ButtonsMenu__pages[start_index], components=[ActionRow(*self._row_of_buttons)]) # allowed_mentions not needed in embeds

        # add row (dynamic menu)
        elif self._menu_type == ButtonsMenu.TypeEmbedDynamic:
            for data_clump in self._chunks(self._dynamic_data_builder, self.__rows_requested):
                joined_data = '\n'.join(data_clump)
                if len(joined_data) <= 2000:
                    possible_block = f"```{self.wrap_in_codeblock}\n{joined_data}```"
                    embed = discord.Embed() if self.custom_embed is None else self.custom_embed.copy()
                    embed.description = joined_data if not self.wrap_in_codeblock else possible_block
                    self._ButtonsMenu__pages.append(embed)
                else:
                    raise DescriptionOversized('With the amount of data that was recieved, the embed description is over discords size limit. Lower the amount of "rows_requested" to solve this problem')
            else:
                # set the main/last pages if any
                if any((self._main_page_contents, self._last_page_contents)):
                    self._ButtonsMenu__pages = collections.deque(self._ButtonsMenu__pages)
                    if self._main_page_contents:
                        self._main_page_contents.reverse()
                        self._ButtonsMenu__pages.extendleft(self._main_page_contents)

                    if self._last_page_contents:
                        self._ButtonsMenu__pages.extend(self._last_page_contents)

                self._refresh_page_director_info(ButtonsMenu.TypeEmbedDynamic, self._ButtonsMenu__pages)

                # make sure data has been added to create at least 1 page
                if not self._ButtonsMenu__pages: raise NoPages('You cannot start a ButtonsMenu when no data has been added')

                self._msg = await self._ctx.send(embed=self._ButtonsMenu__pages[start_index], components=[ActionRow(*self._row_of_buttons)]) # allowed_mentions not needed in embeds

        # add page (text menu)
        else:
            self._refresh_page_director_info(ButtonsMenu.TypeText, self._ButtonsMenu__pages)
            self._msg = await self._ctx.send(content=self._ButtonsMenu__pages[start_index], components=[ActionRow(*self._row_of_buttons)], allowed_mentions=self.allowed_mentions)

        self._pc = _PageController(self._ButtonsMenu__pages)
        self._pc.index = start_index
        self._is_running = True
        self._main_session_task = asyncio.get_event_loop().create_task(self._execute_interactive_session())
        self._main_session_task.add_done_callback(self._done_callback)
