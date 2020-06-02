import discord
import os
import threading

import aiml

from discord.ext import commands
from dotenv import load_dotenv


class SpeechCog(commands.Cog, name='AIML'):
	"""this cog listens for events"""

	def __init__(self, bot: commands.Bot) -> None:
		"""initializer"""

		self.bot = bot
		self.servers = None
		self.nlp = Parser(os.path.join('cogs', 'datasets'))

	# @commands.Cog.listener()
	# async def on_member_join(self, member: discord.Member) -> None:
	#	 """welcomes new members"""

	#	 if not self.servers:
	#		 self.servers = await load_server_dict()
	#	 if not self.servers:
	#		 print('ERROR: server dict is empty after loading', flush=True)
	#		 return
	#	 print('SUCCESS: loaded server dict', flush=True)

	#	 server = member.guild
	#	 if not server:
	#		 print('ERROR: server not found for member', flush=True)
	#		 return

	#	 enabled = ['test', 'main', 'rust']
	#	 servers = {self.servers[x] for x in enabled if x in self.servers}
	#	 if server.id in servers:
	#		 await server.system_channel.send(f'welcome **{member.name}**')

	@commands.Cog.listener()
	async def on_message(self, message):
		"""message listener"""

		# await self.bot.process_commands(message)

		if message.author == self.bot.user:
			return

		server = message.guild

		#------ temporarily disabled speech in direct messages ------#
		if server:
			if discord.utils.get(message.guild.members, id=680692520141062154) in message.mentions:
				processed_message = ' '.join(message.content.split()[1:])
				await message.channel.send(self.nlp.RespondTo(processed_message))


def setup(bot: commands.Bot) -> None:
	bot.add_cog(SpeechCog(bot))


class Parser:
	kernel = None
	datasetdir = ""

	def __init__(self, datasetdir = "datasets"):
		self.kernel = aiml.Kernel()
		self.datasetdir = datasetdir
		self.LoadDataSets()

	def LoadDataSets(self):
		files = os.listdir(self.datasetdir)
		aimlfiles = []
		for x in files:
			if x[-3:] == 'xml':
				self.kernel.learn(os.path.join(self.datasetdir, x))

	def RespondTo(self, message):
		response = self.kernel.respond(message)
		if "{SELF_NAME}" in response: response = response.replace("{SELF_NAME}", "PythonBot")
		if '||' in response:
			command = response[response.index("||"):][12:]
			command_thread = threading.Thread(target=self.HandleCommand, args=(command,))
			command_thread.start()

			returnmessage = response[:response.index("||")]
			return returnmessage
		else:
			return response

	def HandleCommand(self, command):
		# Handle the command here
		print("Command : " + command)
