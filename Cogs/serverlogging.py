import disnake
from disnake.ext import commands
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()  # laad .env-variabelen

class Serverlogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Logging Cog loaded!")

    async def send_to_log(self, message=None, embed=None):
        channel_id = os.getenv("LOG_CHANNEL")
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                await channel.send(content=message, embed=embed)

    async def welcome_func(self, message=None, embed=None):
        channel_id = os.getenv("WELCOME_CHANNEL")
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                await channel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        bot_name = os.getenv("BOT_NAME")
        version = os.getenv("VERSION")
        guild_name = os.getenv("GUILD_NAME")

        embed = disnake.Embed(
            title=f"{bot_name} activated",
            description=f"{bot_name} says **Hi!**\nThis is version {version}.\nGuild name: {guild_name}",
            color=disnake.Color.green(),
            timestamp=dt.datetime.now()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
        embed.add_field(name="Bot Name", value=bot_name, inline=True)
        embed.add_field(name="Version", value=version, inline=True)
        embed.add_field(name="Guild Name", value=guild_name, inline=True)
        embed.add_field(name="Bot Link", value=f"[Jump to bot](https://discord.com/users/{self.bot.user.id})", inline=False)
        embed.set_footer(text=f"Started at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        embed.set_image(url=self.bot.user.display_avatar.url)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        roles = os.getenv('developer'), os.getenv('bots')
        print("Message Deleted")
        embed = disnake.Embed(
            title="🗑️ Message Deleted",
            description=f"{message.content} deleted by {message.author}",
            color=disnake.Color.blue(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
        embed.set_thumbnail(url=message.author.display_avatar.url)
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=message.id, inline=True)
        embed.add_field(name="Message Content", value=message.content, inline=False)
        embed.add_field(name="Message Link", value=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline=False)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        embed = disnake.Embed(
            title="✏️ Message Edited",
            description=f"Edited by: {before.author}",
            color=disnake.Color.blue(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=before.author.name, icon_url=before.author.display_avatar.url)
        embed.set_thumbnail(url=before.author.display_avatar.url)
        embed.add_field(name="Before", value=before.content or "*Empty*", inline=False)
        embed.add_field(name="After", value=after.content or "*Empty*", inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=before.id, inline=True)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(
            title="👋 New Member Joined",
            description=f"{member.mention} just joined **{os.getenv('GUILD_NAME')}**!",
            color=disnake.Color.blurple(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Member ID", value=member.id, inline=True)
        embed.add_field(name="Member Link", value=f"[Jump to user](https://discord.com/users/{member.id})", inline=False)

        await self.send_to_log(embed=embed)
        await self.welcome_func(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = disnake.Embed(
            title="🚪 Member Left",
            description=f"{member.mention} has left the server.",
            color=disnake.Color.red(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Member ID", value=member.id, inline=True)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # ... jouw originele voice logic blijft geldig hier ...
        pass  # vanwege lengte, dit blijft hetzelfde

def setup(bot):
    bot.add_cog(Serverlogging(bot))
