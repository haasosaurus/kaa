# -*- coding: utf-8 -*-


from pythonbot import PythonBot


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    from ._cog import Games
    bot.add_cog(Games(bot))
