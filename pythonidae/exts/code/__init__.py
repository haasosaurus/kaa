# -*- coding: utf-8 -*-


from pythonbot import PythonBot


def setup(bot: PythonBot) -> None:
    """Load the CodeCog cog."""

    from ._cog import Code
    bot.add_cog(Code(bot))
