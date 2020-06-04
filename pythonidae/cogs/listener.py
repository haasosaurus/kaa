# coding=utf-8


#---------------------------- ideas ----------------------------#
# add listener for kick
# add listener for ban
#---------------------------------------------------------------#


import discord
from discord.ext import commands


class ListenerCog(commands.Cog, name='Listener'):
    """this cog listens for events"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """welcomes new members"""

        welcome = self.bot.settings['send_welcome_default']
        default_role = None
        guild_settings = await self.bot.get_guild_settings(member)
        if guild_settings:
            welcome = guild_settings.get('send_welcome', welcome)
            default_role = guild_settings.get('default_role', default_role)

        if welcome:
            await member.guild.system_channel.send(f'welcome **{member.name}**')

        if default_role:
            role = discord.utils.get(member.guild.roles, name=default_role)
            if role:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """says goodbye to members after they've left, pointlessly"""

        goodbye = self.bot.settings['send_goodbye_default']
        guild_settings = await self.bot.get_guild_settings(member)
        if guild_settings:
            goodbye = guild_settings.get('send_goodbye', goodbye)

        if goodbye:
            await member.guild.system_channel.send(f'goodbye forever **{str(member)}**')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ListenerCog(bot))
