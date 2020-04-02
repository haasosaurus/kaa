# coding=utf-8
import random

# import discord
from discord.ext import commands
import discord
from utils import print_context
import cogs.meme_supplements as meme_supplements


class GamesCog(commands.Cog, name="Zi Memes"):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@commands.command(usage='!skill DATA')
	async def skyrim(self, ctx: commands.Context, data):
		
		datasplit = data.split(",")
		print(datasplit)
		if (len(datasplit) >= 2):
			skyrimIns = meme_supplements.SyrimStatusMeme(datasplit[0], datasplit[1])
			skyrimIns.SaveFile("out.png")
			await ctx.send(file=discord.File('out.png'))
		else:
			await ctx.send("Pass 2 comma-separated values to use this")

	@commands.command(usage='!simply THING')
	async def simply(self, ctx: commands.Context, thing):
		meme_supplements.ClassicMemes.oneDoesNotSimply(thing)
		await ctx.send(file=discord.File('out.jpg'))

	@commands.command(usage='!aliens THING')
	async def aliens(self, ctx: commands.Context, thing):
		meme_supplements.ClassicMemes.historyAliensGuy(thing)
		await ctx.send(file=discord.File('out.jpg'))

	@commands.command(usage='!toystory THING')
	async def toystory(self, ctx: commands.Context, thing):
		meme_supplements.ClassicMemes.toyStoryMeme(thing)
		await ctx.send(file=discord.File('out.jpg'))

	
		
def setup(bot: commands.Bot) -> None:
	bot.add_cog(GamesCog(bot))


