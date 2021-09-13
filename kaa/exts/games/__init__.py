# -*- coding: utf-8 -*-


from kaa import Kaa


def setup(bot: Kaa) -> None:
    """function the bot uses to load this extension"""

    from ._cog import Games
    bot.add_cog(Games(bot))
