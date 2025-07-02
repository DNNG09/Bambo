from enum import member
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
import datetime as dt
import logging

client = commands.InteractionBot(intents=disnake.Intents.all())
bot = commands.InteractionBot(intents=disnake.Intents.all())

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
        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )  
        embed.set_author(
            name=self.bot.user.name,
            icon_url=self.bot.user.display_avatar.url
        )
        embed.add_field(name="Bot Name", value=os.getenv('bot_Name'), inline=True)
        embed.add_field(name="Version", value=os.getenv('version'), inline=True)
        embed.add_field(name="Guild Name", value=os.getenv('guild_name'), inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Bot Link", value=f"[Jump to bot](https://discord.com/users/{self.bot.user.id})", inline=False)
        embed.set_footer(text=f"Started at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1310729689022861332/1323576675186900992/Bambo_Logo.png"
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
        embed.set_author(
            name=message.author.name, 
            icon_url=message.author.display_avatar.url
        )  
        embed.set_thumbnail(
            url=message.author.display_avatar.url
        )
        embed.add_field(name="Author", value=message.author.mention, inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=message.id, inline=True)  
        embed.add_field(name="Message Content", value=message.content, inline=False)
        embed.add_field(name="Message Link", value=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline=False)
        

        for role in roles:
            if role not in roles:
                await self.send_to_log(embed=embed)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = disnake.Embed(
            title=f"Message changed",
            description=f"Message changed by: {before.author}",
            color=disnake.Color.blue(),  # 🟦 Messages
            timestamp=dt.datetime.now()
        )
        embed.set_author(
            name=before.author.name, 
            icon_url=before.author.display_avatar.url
        )
        embed.set_thumbnail(
            url=before.author.display_avatar.url
        )
        embed.add_field(name="Before Message", value=before.content, inline=False)
        embed.add_field(name="After Message", value=after.content, inline=False)
        embed.add_field(name="Author", value=before.author.mention, inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        embed.add_field(name="Message ID", value=before.id, inline=True)

        if before.channel == os.getenv('LOG_CHANNEL'):
            return
        else:
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
        embed.add_field(name="Invite Code", value=invite.code, inline=True)
        embed.add_field(name="Channel", value=invite.channel.mention, inline=True)
        embed.add_field(name="Inviter", value=invite.inviter.mention, inline=True)
        embed.add_field(name="Max Uses", value=invite.max_uses, inline=True)
        embed.add_field(name="Expires At", value=invite.expires_at, inline=True)
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(
            title="New Guild member detected!",
            description=f"New user has joined {os.getenv('guild_name')}. Give them a warm welcome in the welcome channel",
            color=disnake.Color.blurple(),  # 🟦 Member changes
            timestamp=dt.datetime.now()
        )
        embed.set_author(
            name=member.name, 
            icon_url=member.display_avatar.url
        )
        embed.set_thumbnail(
            url=member.display_avatar.url
        )  
        embed.add_field(name="Member", value=member.mention, inline=True)  
        embed.add_field(name="Member ID", value=member.id, inline=True)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles if role.name != "@everyone"), inline=False)
        embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)
        embed.set_footer(text=f"Joined at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
            embed.set_author(
                name=after.name, 
                icon_url=after.display_avatar.url  
            )
            embed.set_thumbnail(
                url=after.display_avatar.url
            )
            embed.add_field(name="Member", value=after.mention, inline=True)
            embed.add_field(name="Member ID", value=after.id, inline=True)
            embed.add_field(name="Account Created At", value=after.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=after.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Roles", value=", ".join(role.name for role in after.roles if role.name != "@everyone"), inline=False)
            embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{after.id})", inline=False)
            embed.set_footer(text=f"Updated at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = disnake.Embed(
            title=f"Guild member left: {member.name}",
            description=f"Someone decided that they didn't like us enough and decided to leave {os.getenv('guild_name')}.",
            color=disnake.Color.blurple(),  # 🟦 Member changes
            timestamp=dt.datetime.now()
        )
        embed.set_author(
            name=member.name, 
            icon_url=member.display_avatar.url
        )  
        embed.set_thumbnail(
            url=member.display_avatar.url
        )  
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Member ID", value=member.id, inline=True)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles if role.name != "@everyone"), inline=False)
        embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)
        embed.set_footer(text=f"Left at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = disnake.Embed(
            title="Role Created",
            description=f"New role has been created: {role.mention} ({role.id}).",
            color=disnake.Color.red(),  # 🟥 Roles
            timestamp=dt.datetime.now()
        )
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Role Color", value=str(role.color), inline=True)
        embed.add_field(name="Role Permissions", value=str(role.permissions), inline=False)
        embed.add_field(name="Role Mention", value=role.mention, inline=False)
        embed.set_thumbnail(url=role.icon.url if role.icon else None)

        await self.send_to_log(embed=embed)
        
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
        embed.set_footer(text=f"Updated at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        embed.add_field(name="Role ID", value=after.id, inline=True)
        embed.add_field(name="Role Color", value=str(after.color), inline=True)
        embed.add_field(name="Role Permissions", value=str(after.permissions), inline=False)
        embed.add_field(name="Role Mention", value=after.mention, inline=False)
        embed.set_thumbnail(url=after.icon.url if after.icon else None)

        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = disnake.Embed(
            title="Role has been removed from this server",
            description=f"Role has been removed: {role}.",
            color=disnake.Color.red(),  # 🟥 Roles
            timestamp=dt.datetime.now()
        )
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Role Color", value=str(role.color), inline=True)
        embed.add_field(name="Role Permissions", value=str(role.permissions), inline=False)
        embed.add_field(name="Role Mention", value=role.mention, inline=False)
        embed.set_thumbnail(url=role.icon.url if role.icon else None)

        await self.send_to_log(embed=embed)
        
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
            embed.set_author(
                name=member.name, 
                icon_url=member.display_avatar.url
            )
            embed.set_thumbnail(
                url=member.display_avatar.url
            )
            embed.add_field(name="Voice Channel", value=after.channel.name if after.channel else before.channel.name, inline=False)
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)

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
            embed.set_author(
                name=member.name, 
                icon_url=member.display_avatar.url
            )
            embed.set_thumbnail(
                url=member.display_avatar.url  
            )
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles if role.name != "@everyone"), inline=False)
            embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)

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
            embed.set_author(
                name=member.name, 
                icon_url=member.display_avatar.url
            )  
            embed.set_thumbnail(
                url=member.display_avatar.url
            )   
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

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
            embed.set_author(
                name=member.name, 
                icon_url=member.display_avatar.url
            )
            embed.set_thumbnail(
                url=member.display_avatar.url
            )   
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles if role.name != "@everyone"), inline=False)
            embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)

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
            embed.set_author(
                name=member.name, 
                icon_url=member.display_avatar.url
            )
            embed.set_thumbnail(
                url=member.display_avatar.url
            )
            embed.add_field(name="Member", value=member.mention, inline=True)
            embed.add_field(name="Member ID", value=member.id, inline=True)
            embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Server At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Roles", value=", ".join(role.name for role in member.roles if role.name != "@everyone"), inline=False)
            embed.add_field(name="Member Link", value=f"[Jump to member](https://discord.com/users/{member.id})", inline=False)
            embed.set_footer(text=f"Updated at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            embed.add_field(name="Voice Channel", value=after.channel.name if after.channel else before.channel.name, inline=False)
            embed.add_field(name="Voice Channel ID", value=after.channel.id if after.channel else before.channel.id, inline=True)
            embed.add_field(name="Voice Channel Type", value=after.channel.type.name if after.channel else before.channel.type.name, inline=True)

            await self.send_to_log(embed=embed)

def setup(bot):
    bot.add_cog(Serverlogging(bot))
