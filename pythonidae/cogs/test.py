# coding=utf-8


# standard library modules
#import itertools
#import traceback

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class TestCog(commands.Cog, name='test'):
    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    @print_context
    async def embed(self, ctx: commands.Context) -> None:
        """just a test command"""

        embed = discord.Embed(
            title='test title',
            description='a description',
            color=0x008800
        )
        embed.add_field(name='field 1', value='contents contents contents contents contents contents contents', inline=False)
        embed.set_author(name='Kaa')
        embed.set_footer(text='feet')
        embed.set_image(url='https://cdn.discordapp.com/attachments/796341668458004490/804593492558479360/photo_2020-07-19_02-11-12.jpg')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/796341668458004490/804593492558479360/photo_2020-07-19_02-11-12.jpg')
        print(embed.to_dict())
        await ctx.send(f'hello', embed=embed)


def setup(bot: PythonBot) -> None:
    bot.add_cog(TestCog(bot))
