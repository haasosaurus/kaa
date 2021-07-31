# -*- coding: utf-8 -*-


from pythonbot import PythonBot


def setup(bot: PythonBot) -> None:
    """load the Games extension"""

    from ._cog import Games
    bot.add_cog(Games(bot))
