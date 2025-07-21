import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

class ServerLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ Logging Cog loaded!")

    async def send_log(self, channel_id, embed):
        channel = self.bot.get_channel(int(channel_id))
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"🟢 Bot is ready as {self.bot.user}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        embed = disnake.Embed(title="🗑️ Message Deleted", color=disnake.Color.red())
        embed.add_field(name="User", value=f"{message.author} ({message.author.id})", inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Content", value=message.content or "Embed/attachment", inline=False)
        embed.timestamp = datetime.utcnow()
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        embed = disnake.Embed(title="✏️ Message Edited", color=disnake.Color.orange())
        embed.add_field(name="User", value=f"{before.author} ({before.author.id})", inline=False)
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Before", value=before.content[:1000], inline=False)
        embed.add_field(name="After", value=after.content[:1000], inline=False)
        embed.timestamp = datetime.utcnow()
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(title="✅ Member Joined", description=f"{member.mention} ({member.id})", color=disnake.Color.green(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = disnake.Embed(title="❌ Member Left", description=f"{member.mention} ({member.id})", color=disnake.Color.red(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        changes = []
        if before.channel != after.channel:
            if after.channel is None:
                changes.append(f"🔈 Left voice channel: `{before.channel}`")
            elif before.channel is None:
                changes.append(f"🔊 Joined voice channel: `{after.channel}`")
            else:
                changes.append(f"🔁 Switched voice channel: `{before.channel}` → `{after.channel}`")

        if before.self_mute != after.self_mute:
            changes.append(f"🎙️ Mic {'muted' if after.self_mute else 'unmuted'}")

        if before.self_deaf != after.self_deaf:
            changes.append(f"🔇 Deafened: {after.self_deaf}")

        if before.self_video != after.self_video:
            changes.append(f"📷 Camera {'enabled' if after.self_video else 'disabled'}")

        if before.self_stream != after.self_stream:
            changes.append(f"📺 Streaming {'started' if after.self_stream else 'stopped'}")

        if changes:
            embed = disnake.Embed(title="🎧 Voice Update", description="\n".join(changes), color=disnake.Color.blurple(), timestamp=datetime.utcnow())
            embed.set_author(name=str(member), icon_url=member.display_avatar.url)
            await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        embed = disnake.Embed(title="👤 Member Update", color=disnake.Color.blue(), timestamp=datetime.utcnow())
        changes = []

        if before.nick != after.nick:
            changes.append(f"🔤 Nickname: `{before.nick}` → `{after.nick}`")

        before_roles = set(before.roles)
        after_roles = set(after.roles)

        added = after_roles - before_roles
        removed = before_roles - after_roles

        if added:
            changes.append(f"➕ Roles added: {', '.join(role.mention for role in added)}")
        if removed:
            changes.append(f"➖ Roles removed: {', '.join(role.mention for role in removed)}")

        if changes:
            embed.description = "\n".join(changes)
            embed.set_author(name=str(after), icon_url=after.display_avatar.url)
            await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = disnake.Embed(title="🚫 Member Banned", description=f"{user.mention} ({user.id})", color=disnake.Color.dark_red(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = disnake.Embed(title="♻️ Member Unbanned", description=f"{user.mention} ({user.id})", color=disnake.Color.green(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        embed = disnake.Embed(title="🏛️ Server Updated", color=disnake.Color.gold(), timestamp=datetime.utcnow())
        if before.name != after.name:
            embed.add_field(name="Naam", value=f"`{before.name}` → `{after.name}`", inline=False)
        if before.icon != after.icon:
            embed.set_thumbnail(url=after.icon.url)
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        embed = disnake.Embed(title="📢 Channel Updated", description=f"{after.mention} ({after.id})", color=disnake.Color.purple(), timestamp=datetime.utcnow())
        if before.name != after.name:
            embed.add_field(name="Naam", value=f"`{before.name}` → `{after.name}`", inline=False)
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        embed = disnake.Embed(title="➕ Reaction Added", description=f"{user.mention} reacted with {reaction.emoji}", color=disnake.Color.green(), timestamp=datetime.utcnow())
        embed.add_field(name="Channel", value=reaction.message.channel.mention)
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        embed = disnake.Embed(title="➖ Reaction Removed", description=f"{user.mention} removed {reaction.emoji}", color=disnake.Color.red(), timestamp=datetime.utcnow())
        embed.add_field(name="Channel", value=reaction.message.channel.mention)
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        embed = disnake.Embed(title="🧵 Thread Created", description=f"{thread.mention}", color=disnake.Color.green(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        embed = disnake.Embed(title="✏️ Thread Updated", description=f"{after.mention}", color=disnake.Color.orange(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        embed = disnake.Embed(title="❌ Thread Deleted", description=f"{thread.name}", color=disnake.Color.red(), timestamp=datetime.utcnow())
        await self.send_log(os.getenv("LOG_CHANNEL"), embed)

def setup(bot):
    bot.add_cog(ServerLogging(bot))
