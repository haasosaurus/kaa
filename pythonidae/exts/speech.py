# -*- coding: utf-8 -*-


# standard library modules
import pathlib
import threading

# third-party packages
import aiml

# third-party packages - discord related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot


class Speech(commands.Cog, name='speech'):
    """this cog listens for events"""

    def __init__(self, bot: PythonBot) -> None:
        """initializer"""

        self.bot = bot
        self.servers = None
        datasets_path = pathlib.Path('resources/data/aiml/datasets')
        self.nlp = Parser(datasets_path)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """message listener"""

        if message.author == self.bot.user:
            return

        server = message.guild
        command_message = None
        if server:
            if discord.utils.get(message.guild.members, id=self.bot.user.id) in message.mentions:
                command_message = message
        else:
            if not message.content.startswith('!'):
                command_message = message

        if command_message:
            processed_message = ' '.join(x for x in command_message.content.split() if str(self.bot.user.id) not in x)
            reply = self.nlp.RespondTo(processed_message).replace('[newline]', '\n')
            await command_message.channel.send(reply)


def setup(bot: PythonBot) -> None:
    """
    function the bot uses to load this extension
    """

    bot.add_cog(Speech(bot))


class Parser:
    def __init__(self, datasets_path: pathlib.Path) -> None:
        self.kernel = aiml.Kernel()
        self.datasets_path = datasets_path
        self.LoadDataSets()

    def LoadDataSets(self) -> None:
        for p in self.datasets_path.iterdir():
            if p.is_file() and p.suffix == '.xml':
                self.kernel.learn(str(p))

    def RespondTo(self, message: str) -> str:
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

    def HandleCommand(self, command) -> None:
        # Handle the command here
        print("Command : " + command)
