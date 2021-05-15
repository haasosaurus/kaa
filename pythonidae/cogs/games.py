# coding=utf-8


import random

# import discord
from discord.ext import commands

from utils import print_context


class GamesCog(commands.Cog, name='games'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(
        aliases=['dice_roll', 'roll', 'roll_dice'],
        usage='!roll AMOUNT SIDES',

    )
    @print_context
    async def dice(
            self,
            ctx: commands.Context,
            amount: int = None,
            sides: int = None
    ) -> None:
        """simulates rolling AMOUNT dice with SIDES sides"""

        amount = amount if amount else 1
        sides = sides if sides else 6
        if (0 < amount <= 100) and (1 < sides <= 1000):
            msg = ', '.join(str(random.randint(1, sides)) for _ in range(amount))
            await self.bot.send_info_msg(ctx, msg)
        else:
            msg = 'ranges are: 0 < AMOUNT <= 100, 1 < SIDES <= 1000'
            await self.bot.send_error_msg(ctx, msg)

    @commands.command(aliases=['coin_flip', 'flip', 'flip_coin'])
    @print_context
    async def coin(self, ctx: commands.Context) -> None:
        """simulates flipping a coin"""

        msg = random.choice(['heads', 'tails'])
        await self.bot.send_info_msg(ctx, msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GamesCog(bot))
