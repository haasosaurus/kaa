# coding=utf-8


import random

# import discord
from discord.ext import commands


class GamesCog(commands.Cog, name="Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', help='simulates rolling a variable amount of dice with a variable amount of sides')
    async def roll(self, ctx, amount: int = None, sides: int = None):
        amount = amount or 1
        sides = sides or 6
        if (0 < amount <= 100) and (0 < sides <= 1000):
            dice = [
                str(random.choice(range(1, sides + 1)))
                for _ in range(amount)
            ]
            response = '**`' + ', '.join(dice) + '`**'
        else:
            response = '**`ERROR: AMOUNT and SIDES must be in these ranges: 0 < AMOUNT <= 100, 0 < SIDES <= 1000`**'
        await ctx.send(response)


def setup(bot):
    bot.add_cog(GamesCog(bot))
