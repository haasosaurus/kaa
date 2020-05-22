# coding=utf-8


# This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
# However, you must put:
# bot.remove_command('help')
# in your bot, and the command must be in a cog for it to work.
# Written by Jared Newsom (AKA Jared M.F


import discord
from discord.ext import commands

from utils import print_context


class HelpCog(commands.Cog, name='help_cog'):
    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    # @commands.command(name='custom_help', pass_context=True)
    # @commands.has_permissions(add_reactions=True,embed_links=True)
    # async def custom_help(self, ctx, *cog):
    #     """Gets all cogs and commands of mine."""
    #     try:
    #         if not cog:
    #             """Cog listing.  What more?"""
    #             halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
    #                             description='Use `!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
    #             cogs_desc = ''
    #             for x in self.bot.cogs:
    #                 cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
    #             halp.add_field(name='Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
    #             cmds_desc = ''
    #             for y in self.bot.walk_commands():
    #                 if not y.cog_name and not y.hidden:
    #                     cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
    #             halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
    #             await ctx.message.add_reaction(emoji='✉')
    #             await ctx.message.author.send('',embed=halp)
    #         else:
    #             """Helps me remind you if you pass too many args."""
    #             if len(cog) > 1:
    #                 halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
    #                 await ctx.message.author.send('',embed=halp)
    #             else:
    #                 """Command listing within a cog."""
    #                 found = False
    #                 for x in self.bot.cogs:
    #                     for y in cog:
    #                         if x == y:
    #                             halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
    #                             for c in self.bot.get_cog(y).get_commands():
    #                                 if not c.hidden:
    #                                     halp.add_field(name=c.name,value=c.help,inline=False)
    #                             found = True
    #                 if not found:
    #                     """Reminds you if that cog doesn't exist."""
    #                     halp = discord.Embed(title='Error!',description='How do you even use \''+cog[0]+'\'?',color=discord.Color.red())
    #                 else:
    #                     await ctx.message.add_reaction(emoji='✉')
    #                 await ctx.message.author.send('',embed=halp)
    #     except:
    #         await ctx.send("Excuse me, I can't send embeds.")


    # @commands.command(name='custom_help', pass_context=True)
    # @commands.has_permissions(add_reactions=True,embed_links=True)
    # @commands.command(name='custom_help')
    # async def custom_help(self, ctx, cog: str = None, *subcommands: str):
    #     """Gets all cogs and commands of mine."""

    #     try:
    #         if not cog:
    #             """Cog listing.  What more?"""
    #             halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
    #                             description='Use `!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
    #             cogs_desc = ''
    #             for x in self.bot.cogs:
    #                 cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
    #             halp.add_field(name='Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
    #             cmds_desc = ''
    #             for y in self.bot.walk_commands():
    #                 if not y.cog_name and not y.hidden:
    #                     cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
    #             halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
    #             await ctx.message.add_reaction(emoji='✉')
    #             await ctx.message.author.send('',embed=halp)
    #         else:
    #             """Helps me remind you if you pass too many args."""
    #             if len(cog) > 1:
    #                 halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
    #                 await ctx.message.author.send('',embed=halp)
    #             else:
    #                 """Command listing within a cog."""
    #                 found = False
    #                 for x in self.bot.cogs:
    #                     for y in cog:
    #                         if x == y:
    #                             halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
    #                             for c in self.bot.get_cog(y).get_commands():
    #                                 if not c.hidden:
    #                                     halp.add_field(name=c.name,value=c.help,inline=False)
    #                             found = True
    #                 if not found:
    #                     """Reminds you if that cog doesn't exist."""
    #                     halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
    #                 else:
    #                     await ctx.message.add_reaction(emoji='✉')
    #                 await ctx.message.author.send('',embed=halp)
    #     except:
    #         await ctx.send("Excuse me, I can't send embeds.")


    @commands.command(name='custom_help')
    async def custom_help(self, ctx, *args):
        pages = self.bot.formatter.format_help_for(ctx, self.bot)
        commands.HelpCommand(context=ctx, show_hidden=True, )



# def setup(bot):
#     bot.add_command(help)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelpCog(bot))
