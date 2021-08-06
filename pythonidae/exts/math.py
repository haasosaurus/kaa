# -*- coding: utf-8 -*-


# standard library modules
import io
from typing import List, Union

# third-party packages
from PIL import Image
from pytexit import py2tex
import sympy

# third-party packages - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot
from utils import print_context


class Math(commands.Cog, name='test'):
    def __init__(self, bot: PythonBot) -> None:
        self.bot = bot

        self.embed_color = 0xfed142

    @commands.command()
    @print_context
    async def tex(self, ctx: commands.Context, *, expression: str) -> None:
        """
        turn python math expression into latex image in an embed
        ex: !tex x = 2 * sqrt(2 * pi * k * T_e / m_e) * (DeltaE / (k * T_e))**2 * a_0**2
        """

        # strip any whitespace and backticks
        expression = expression.strip().strip('`').strip()

        # converts python math expression to latex string
        try:
            tex = py2tex(
                expression,
                print_latex=False,
                print_formula=False,
            )
        except (TypeError, SyntaxError):
            return await self.bot.send_error_msg(ctx, 'Expression could not be processed')

        # convert latex to png and save to buffer
        buffer = io.BytesIO()
        sympy.preview(
            tex,
            viewer='BytesIO',
            outputbuffer=buffer,
            euler=False,
            dvioptions=[
                "-T", "tight",
                "-z", "0",
                "--truecolor",
                "-D 400",
                "-bg", "Transparent",
                "-fg", "White",
            ],
        )

        # open buffer as PIL.Image
        img = Image.open(buffer)

        # if the image width is higher than width
        width = 400
        if img.width > width:

            # resize image to width preserving aspect ratio
            img.thumbnail(size=(width, 1000))

        # add padding to the image
        pad_h = 20
        pad_v = 20
        w = img.width + pad_h * 2
        h = img.height + pad_v * 2
        padded_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        padded_img.paste(img, (pad_h, pad_v))

        # clear the buffer
        buffer.seek(0)
        buffer.truncate(0)

        # write the resized/padded image to the cleared buffer
        padded_img.save(buffer, format='PNG')

        # seek to the beginning of the buffer
        buffer.seek(0)

        # use it to initialize a discord.File object
        file = discord.File(fp=buffer, filename='tex.png')

        # create embed for the latex image to be sent in
        embed = discord.Embed(
            title='Python Math Expression to Latex',
            color=self.embed_color,
        )
        embed.set_image(url="attachment://tex.png")

        # send the embed and the image as an attachment
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @print_context
    async def tex_test(self, ctx: commands.Context) -> None:
        """test for the tex command"""

        expression = 'x = 2 * sqrt(2 * pi * k * T_e / m_e) * (DeltaE / (k * T_e))**2 * a_0**2'
        await ctx.invoke(self.bot.get_command('tex'), expression=expression)


def setup(bot: PythonBot) -> None:
    bot.add_cog(Math(bot))
