# coding=utf-8


import random

# import discord
from discord.ext import commands


class GamesCog(commands.Cog, name="Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', help='simulates rolling dice')
    async def roll(self, ctx, number_of_dice: int = None, number_of_sides: int = None):
        number_of_dice = number_of_dice or 1
        number_of_sides = number_of_sides or 6
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


def setup(bot):
    bot.add_cog(GamesCog(bot))
