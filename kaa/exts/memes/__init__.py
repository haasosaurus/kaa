# -*- coding: utf-8 -*-


import importlib

from kaa import Kaa
from . import _meme_generator


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    importlib.reload(_meme_generator)
    from ._cog import Memes
    bot.add_cog(Memes(bot))
