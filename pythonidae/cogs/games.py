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
        if number_of_dice > 100 or number_of_sides > 1000:
            response = 'number of dice must be <= 100, number of sides must be <= 1000'
        else:
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            response = '```' + ', '.join(dice) + '```'
        await ctx.send(response)


def setup(bot):
    bot.add_cog(GamesCog(bot))
