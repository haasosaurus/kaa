# coding=utf-8


#---------------------------- ideas ----------------------------#
#
#---------------------------------------------------------------#


from typing import Union

import discord
from discord.ext import commands


class ListenerCog(commands.Cog, name='Listener'):
    """this cog listens for events"""

    def __init__(self, bot: commands.Bot) -> None:
        """ListenerCog initializer"""

        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """
        Called when a Member joins a Guild.
        welcomes new members
        """

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
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    msg = '**`ERROR: incorrect permissions to set default guild role`**'
                    await member.guild.system_channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """
        Called when a Member leaves a Guild.
        says goodbye to members after they've left, pointlessly
        """

        # send kick info if bot has correct permissions
        try:
            async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=3):
                if entry.target == member:
                    msg = (
                        f'**`{entry.user} kicked {entry.target}, '
                        f"reason given: '{entry.reason.strip() if entry.reason else 'none'}'`**"
                    )
                    await member.guild.system_channel.send(msg)
                    break
        except discord.Forbidden:
            pass

        # send goodbye if enabled for member's guild
        goodbye = self.bot.settings['send_goodbye_default']
        guild_settings = await self.bot.get_guild_settings(member)
        if guild_settings:
            goodbye = guild_settings.get('send_goodbye', goodbye)

        if goodbye:
            await member.guild.system_channel.send(f'goodbye forever **{member}**')

    @commands.Cog.listener()
    @commands.has_permissions(view_audit_log=True)
    async def on_member_ban(
            self,
            guild: discord.Guild,
            user: Union[discord.User, discord.Member]
    ) -> None:
        """
        Called when user gets banned from a Guild.
        """

        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=3):
            if entry.target == user:
                msg = (
                    f'**`{entry.user} banned {entry.target}, '
                    f"reason given: '{entry.reason.strip() if entry.reason else 'none'}'`**"
                )
                await guild.system_channel.send(msg)
                break

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Called when the Client joins a guild."""

        msg = f"joined server: '{guild.name}', id: {guild.id}"
        print(msg)
        owner = await self.bot.get_owner()
        await owner.send(msg)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """
        Called when a Guild is removed from the Client.
        ex: The client got banned, kicked, left, guild deleted
        """

        msg = f"left server: '{guild.name}', id: {guild.id}"
        print(msg)
        owner = await self.bot.get_owner()
        await owner.send(msg)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild) -> None:
        """Called when a guild becomes available."""

        msg = f"server status is now AVAILABLE: '{guild.name}', id: {guild.id}"
        print(msg)
        # owner = await self.bot.get_owner()
        # await owner.send(msg)

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild: discord.Guild) -> None:
        """Called when a guild becomes unavailable."""

        msg = f"server status is now UNAVAILABLE: '{guild.name}', id: {guild.id}"
        print(msg)
        owner = await self.bot.get_owner()
        await owner.send(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ListenerCog(bot))
