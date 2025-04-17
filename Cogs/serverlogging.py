import disnake
from disnake.ext import commands
from env import Guild_Data, Channels
import datetime as dt
import logging

client = disnake.client
bot = commands.Bot(intents=disnake.Intents.all())

user = disnake.guild.User

class Serverlogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Logging Cog is loaded!")

    async def send_to_log(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(Channels.log_channel)
        await channel.send(content=message, embed=embed)
    
    async def welcome_func(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(Channels.welcome_channel)
        await channel.send(content=message, embed=embed)
 

    @commands.Cog.listener()
    async def on_ready(self):
        embed = disnake.Embed(title=f"{Guild_Data.bot_Name} activated", description=f"{Guild_Data.bot_Name} says **Hi!** \n This is version {Guild_Data.version}. \n Guild name: {Guild_Data.guild_name}", color=disnake.Color.green(), timestamp=dt.datetime.now())
        await self.send_to_log(embed=embed)
        logging.info(f"{Guild_Data.bot_Name} is online")
        

    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print ("Message Deleted")
        embed = disnake.Embed(title="Message Removed", description=f"{message.content} deleted by {message.author}", color=disnake.Color.blue(), timestamp=dt.datetime.now())
        await self.send_to_log(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = disnake.Embed(title="Message Edit", description=f"{before.content} is changed into {after.content}", color=disnake.Color.blue(), timestamp=dt.datetime.now())
        await self.send_to_log(embed=embed)   
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = disnake.Embed(title="Invite created", description=f"A new invite has been created: {invite}", color=disnake.Color.orange(), timestamp=dt.datetime.now())
        await self.send_to_log(embed=embed) 

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        embed = disnake.Embed(title="Invite removed", description=f"An invite has been removed: {invite}", color=disnake.Color.orange(), timestamp=dt.datetime.now())
        await self.send_to_log(embed=embed) 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(title="New Guild member detected!", description=f"New user has joined {Guild_Data.guild_name}. Give them a warm welcome in the welcome channel", color=disnake.Colour.dark_purple(), timestamp= dt.datetime.now())
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.roles != after.roles:
            embed = disnake.Embed(title=f"Guild member updated: {after.name}", description=f"**Before:** {[role.name for role in before.roles]}\n**After:** {[role.name for role in after.roles]}", color=disnake.Colour.dark_purple(), timestamp=dt.datetime.now())
            await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = disnake.Embed(title=f"Guild member left: {member.name}", description=f"Someone decided that they didn't like us enough and decided to leave {Guild_Data.guild_name}.", color=disnake.Colour.dark_purple(), timestamp= dt.datetime.now())
        await self.send_to_log(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = disnake.Embed(title="Role Created", description=f"New role has been created: {role.mention} ({role.id}).", color=disnake.Colour.red(), timestamp= dt.datetime.now())
        await self.send_to_log(embed=embed)
        print (f"{role} has been created")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        embed = disnake.Embed(title="Role has been updated", description= f"{before} has changed.", color=disnake.Colour.red(), timestamp= dt.datetime.now())
        embed.add_field(name=f"Name before: {before}", value=" ", inline=False)
        embed.add_field(name=f"Name after: {after}", value=" ", inline=False)
        await self.send_to_log(embed=embed)
        print ("Role changed")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = disnake.Embed(title="Role has been removed from this server", description= f"Role has been removed: {role}.", color=disnake.Colour.red(), timestamp= dt.datetime.now())
        await self.send_to_log(embed=embed)
        print ("Role deleted")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        embed = disnake.Embed(title="VC has been updated", description= f"{member.name} has joined VC: {after.channel}. Before: {before.channel}", color=disnake.Colour.yellow(), timestamp= dt.datetime.now())
        await self.send_to_log(embed=embed)
        print(f"{member} has left VC {before} and you can find the user in {after.channel}")

def setup(bot):
    bot.add_cog(Serverlogging(bot))