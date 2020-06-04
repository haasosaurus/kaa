# coding=utf-8


import random

# import discord
from discord.ext import commands

from utils import print_context


class GamesCog(commands.Cog, name='Game Commands'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        aliases=['dice', 'roll', 'roll_dice'],
        usage='!roll AMOUNT SIDES',

    )
    @print_context
    async def dice_roll(
            self,
            ctx: commands.Context,
            amount: int = None,
            sides: int = None
    ) -> None:
        """simulates rolling AMOUNT dice with SIDES sides"""

        amount = amount if amount else 1
        sides = sides if sides else 6
        if (0 < amount <= 100) and (1 < sides <= 1000):
            dice = [str(random.randint(1, sides)) for _ in range(amount)]
            msg = '**`' + ', '.join(dice) + '`**'
        else:
            msg = '**`ERROR: ranges are: 0 < AMOUNT <= 100, 1 < SIDES <= 1000`**'
        await ctx.send(msg)

    @commands.command(aliases=['coin', 'flip', 'flip_coin'])
    @print_context
    async def coin_flip(self, ctx: commands.Context) -> None:
        """simulates flipping a coin"""

        side = random.choice(['heads', 'tails'])
        msg = f'**`{side}`**'
        await ctx.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GamesCog(bot))
