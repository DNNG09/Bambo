import disnake
from disnake.ext import commands
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

class Serverlogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Logging Cog loaded!")

    async def send_to_log(self, message=None, embed=None):
        channel_id = os.getenv("LOG_CHANNEL")
        if channel_id:
            try:
                channel = await self.bot.fetch_channel(int(channel_id))
                await channel.send(content=message, embed=embed)
            except Exception as e:
                print(f"❌ Error sending to log channel: {e}")

    async def welcome_func(self, message=None, embed=None):
        channel_id = os.getenv("WELCOME_CHANNEL")
        if channel_id:
            try:
                channel = await self.bot.fetch_channel(int(channel_id))
                await channel.send(content=message, embed=embed)
            except Exception as e:
                print(f"❌ Error sending to welcome channel: {e}")

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
        print("🗑️ Message Deleted")
        content = message.content or "*Empty*"
        if len(content) > 1024:
            content = content[:1021] + "..."

        embed = disnake.Embed(
            title="🗑️ Message Deleted",
            description=f"Deleted by: {message.author}",
            color=disnake.Color.blue(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
        embed.set_thumbnail(url=message.author.display_avatar.url)
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=message.id, inline=True)
        embed.add_field(name="Message Content", value=content, inline=False)
        embed.add_field(name="Message Link", value=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline=False)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return

        content_before = before.content or "*Empty*"
        content_after = after.content or "*Empty*"
        if len(content_before) > 1024:
            content_before = content_before[:1021] + "…"
        if len(content_after) > 1024:
            content_after = content_after[:1021] + "…"

        embed = disnake.Embed(
            title="✏️ Message Edited",
            description=f"Edited by: {before.author}",
            color=disnake.Color.blue(),
            timestamp=dt.datetime.now()
        )
        embed.set_author(name=before.author.name, icon_url=before.author.display_avatar.url)
        embed.set_thumbnail(url=before.author.display_avatar.url)
        embed.add_field(name="Before", value=content_before, inline=False)
        embed.add_field(name="After", value=content_after, inline=False)
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
        # Optioneel: hier kun je voice join/leave logica toevoegen
        pass

def setup(bot):
    bot.add_cog(Serverlogging(bot))
