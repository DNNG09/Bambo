import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import datetime as dt
import logging

client = disnake.client
bot = commands.Bot(intents=disnake.Intents.all())

load_dotenv()

user = disnake.guild.User

class Serverlogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Logging Cog is loaded!")

    async def send_to_log(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(os.getenv('log_channel'))
        await channel.send(content=message, embed=embed)
    
    async def welcome_func(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(os.getenv('welcome_channel'))
        await channel.send(content=message, embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        embed = disnake.Embed(
            title=f"{os.getenv('bot_Name')} activated",
            description=f"{os.getenv('bot_Name')} says **Hi!** \nThis is version {os.getenv('version')}. \nGuild name: {os.getenv('guild_name')}",
            color=disnake.Color.green(),  # ✅ Startup / status
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)
        logging.info(f"{os.getenv('bot_Name')} is online")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        roles = os.getenv('admin_1'), os.getenv('admin_2'), os.getenv('bots')
        print("Message Deleted")
        embed = disnake.Embed(
            title="Message Removed",
            description=f"{message.content} deleted by {message.author}",
            color=disnake.Color.blue(),  # 🟦 Messages
            timestamp=dt.datetime.now()
        )
        for role in roles:
            if role not in roles:
                await self.send_to_log(embed=embed)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = disnake.Embed(
            title=f"Message changed in: {before.channel} \n Changed bij {before.author}",
            description=f"Message before: {before.content} \nMessage after: {after.content}",
            color=disnake.Color.blue(),  # 🟦 Messages
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = disnake.Embed(
            title="Invite created",
            description=f"A new invite has been created: {invite}",
            color=disnake.Color.gold(),  # 🟨 Invites
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        embed = disnake.Embed(
            title="Invite removed",
            description=f"An invite has been removed: {invite}",
            color=disnake.Color.gold(),  # 🟨 Invites
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(
            title="New Guild member detected!",
            description=f"New user has joined {os.getenv('guild_name')}. Give them a warm welcome in the welcome channel",
            color=disnake.Color.blurple(),  # 🟦 Member changes
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.roles != after.roles:
            embed = disnake.Embed(
                title=f"Guild member updated: {after.name}",
                description=f"**Before:** {[role.name for role in before.roles]}\n**After:** {[role.name for role in after.roles]}",
                color=disnake.Color.blurple(),  # 🟦 Member changes
                timestamp=dt.datetime.now()
            )
            await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = disnake.Embed(
            title=f"Guild member left: {member.name}",
            description=f"Someone decided that they didn't like us enough and decided to leave {os.getenv('guild_name')}.",
            color=disnake.Color.blurple(),  # 🟦 Member changes
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = disnake.Embed(
            title="Role Created",
            description=f"New role has been created: {role.mention} ({role.id}).",
            color=disnake.Color.red(),  # 🟥 Roles
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)
        print(f"{role} has been created")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        embed = disnake.Embed(
            title="Role has been updated",
            description=f"{before} has changed.",
            color=disnake.Color.red(),  # 🟥 Roles
            timestamp=dt.datetime.now()
        )
        embed.add_field(name=f"Name before: {before}", value=" ", inline=False)
        embed.add_field(name=f"Name after: {after}", value=" ", inline=False)
        await self.send_to_log(embed=embed)
        print("Role changed")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = disnake.Embed(
            title="Role has been removed from this server",
            description=f"Role has been removed: {role}.",
            color=disnake.Color.red(),  # 🟥 Roles
            timestamp=dt.datetime.now()
        )
        await self.send_to_log(embed=embed)
        print("Role deleted")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        timestamp = dt.datetime.now()

        # VC Join / Leave / Move
        if before.channel != after.channel:
            if before.channel is None and after.channel is not None:
                event = "joined a voice channel"
                description = f"{member.mention} joined **{after.channel.name}**"
            elif before.channel is not None and after.channel is None:
                event = "left a voice channel"
                description = f"{member.mention} left **{before.channel.name}**"
            else:
                event = "moved voice channels"
                description = f"{member.mention} moved from **{before.channel.name}** to **{after.channel.name}**"

            embed = disnake.Embed(
                title=event.capitalize(),
                description=description,
                color=disnake.Color.teal(),  # 🟩 Voice movement
                timestamp=timestamp
            )
            await self.send_to_log(embed=embed)

        # Mic mute/unmute
        if before.self_mute != after.self_mute:
            state = "muted" if after.self_mute else "unmuted"
            embed = disnake.Embed(
                title="Microphone Status Changed",
                description=f"{member.mention} has **{state}** their mic.",
                color=disnake.Color.orange(),  # 🟧 Mic
                timestamp=timestamp
            )
            await self.send_to_log(embed=embed)

        # Headphones deafen/undeafen
        if before.self_deaf != after.self_deaf:
            state = "deafened" if after.self_deaf else "undeafened"
            embed = disnake.Embed(
                title="Headphones Status Changed",
                description=f"{member.mention} has **{state}** themselves.",
                color=disnake.Color.dark_orange(),  # 🟫 Deaf
                timestamp=timestamp
            )
            await self.send_to_log(embed=embed)

        # Video cam on/off
        if before.self_video != after.self_video:
            state = "enabled" if after.self_video else "disabled"
            embed = disnake.Embed(
                title="Camera Status Changed",
                description=f"{member.mention} has **{state}** their camera.",
                color=disnake.Color.magenta(),  # 🟪 Cam
                timestamp=timestamp
            )
            await self.send_to_log(embed=embed)

        # Screen share on/off
        if before.self_stream != after.self_stream:
            state = "started" if after.self_stream else "stopped"
            embed = disnake.Embed(
                title="Screen Share Status Changed",
                description=f"{member.mention} has **{state}** screen sharing.",
                color=disnake.Color.dark_green(),  # 🟩 Screenshare
                timestamp=timestamp
            )
            await self.send_to_log(embed=embed)

def setup(bot):
    bot.add_cog(Serverlogging(bot))
