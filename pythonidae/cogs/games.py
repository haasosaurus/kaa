# coding=utf-8


import random

# import discord
from discord.ext import commands

from utils import print_context


class GamesCog(commands.Cog, name='Game Commands'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(aliases=['dice', 'roll_dice'], usage='!roll AMOUNT SIDES')
    @print_context
    async def roll(
            self,
            ctx: commands.Context,
            amount: int = None,
            sides: int = None
    ) -> None:
        """simulates rolling AMOUNT dice with SIDES sides"""

        amount = amount or 1
        sides = sides or 6
        if (0 < amount <= 100) and (0 < sides <= 1000):
            dice = [
                str(random.choice(range(1, sides + 1)))
                for _ in range(amount)
            ]
            msg = '**`' + ', '.join(dice) + '`**'
        else:
            msg = '**`ERROR: ranges are: 0 < AMOUNT <= 100, 0 < SIDES <= 1000`**'
        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GamesCog(bot))
