# -*- coding: utf-8 -*-


# standard library modules
import importlib

# local modules
from . import _codeformatter
from pythonbot import PythonBot


def setup(bot: PythonBot) -> None:
    """function the bot uses to load this extension"""

    from ._cog import Code
    importlib.reload(_codeformatter)
    bot.add_cog(Code(bot))
