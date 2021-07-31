# -*- coding: utf-8 -*-


# standard library modules
import sys
import traceback

# third-party modules - discord and related
import discord
from discord.ext import commands

# local modules
from pythonbot import PythonBot


class CommandErrorHandler(commands.Cog):
    """cog for handling errors that aren't caught by command specific error handlers"""

    def __init__(self, bot: PythonBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: BaseException):
        """triggered when an error is raised while invoking a command"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            msg = f"'{ctx.command}' has been disabled."
            return await self.bot.send_error_msg(ctx, msg)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                msg = f"'{ctx.command}' can't be used in private messages."
                return await self.bot.send_error_msg(ctx, msg)
            except:
                pass

        elif isinstance(error, commands.PrivateMessageOnly):
            try:
                msg = f"'{ctx.command}' can only be used in private messages."
                return await self.bot.send_error_msg(ctx, msg)
            except:
                pass

        elif isinstance(error, commands.NotOwner):
            msg = f"You must be the bot's owner to run '{ctx.command}'."
            return await self.bot.send_error_msg(ctx, msg)

        elif isinstance(error, commands.MissingRole):
            msg = f"You're missing a role required to run '{ctx.command}'."
            return await self.bot.send_error_msg(ctx, msg)

        elif isinstance(error, commands.MissingPermissions):
            msg = f"You don't have permission to run '{ctx.command}'."
            return await self.bot.send_error_msg(ctx, msg)

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot: PythonBot) -> None:
    bot.add_cog(CommandErrorHandler(bot))
