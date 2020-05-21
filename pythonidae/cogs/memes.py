# coding=utf-8


import io
import random

import discord
from discord.ext import commands

from memegenerator import MemeGenerator
from utils import print_context


class GamesCog(commands.Cog, name='Memes'):
	def __init__(self, bot: commands.Bot) -> None:
		"""initializer"""

		self.bot = bot
		self.generator = MemeGenerator()

	@commands.command(usage='!skill SKILL LEVEL')
	@print_context
	async def skyrim(
			self,
			ctx: commands.Context,
			skill: str,
			level: str,
			*args: str
	) -> None:
		"""!skyrim SKILL LEVEL"""

		img_buf = self.generator.skyrim(skill, level)
		await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

	@commands.command(usage='!simply *WORDS')
	@print_context
	async def simply(self, ctx: commands.Context, *words: str) -> None:
		"""!simply *WORDS"""

		text = ' '.join(words)
		img_buf = self.generator.oneDoesNotSimply(text)
		await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

	@commands.command(usage='!aliens *WORDS')
	@print_context
	async def aliens(self, ctx: commands.Context, *words: str) -> None:
		"""!aliens *WORDS"""

		text = ' '.join(words)
		img_buf = self.generator.historyAliensGuy(text)
		await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))

	@commands.command(aliases=['buzz'], usage='!toystory *WORDS')
	@print_context
	async def toystory(self, ctx: commands.Context, *words: str) -> None:
		"""!toystory *WORDS"""

		text = ' '.join(words)
		img_buf = self.generator.toyStoryMeme(text)
		await ctx.send(file=discord.File(fp=img_buf, filename='image.png'))


def setup(bot: commands.Bot) -> None:
	bot.add_cog(GamesCog(bot))
