from disnake.ext import commands, tasks
from env import Channels
from datetime import datetime, timedelta, timezone


class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_bump_time = None
        self.bump_channel_id = Channels.bump
        self.bump_interval = timedelta(hours=2)
        print("Loaded Cog bump")

    async def send_to_log(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(Channels.log_channel)
        await channel.send(content=message, embed=embed)
    
    async def send_to_bump(self, message=None, embed=None):
        channel = await self.bot.fetch_channel(Channels.bump)
        await channel.send(content=message, embed=embed)

    @tasks.loop(minutes=5)
    async def check_bump(self):
        channel = Channels.bump
        if not channel:
            self.send_to_log("Error in check_bump: Channel not found")
            return

        if self.last_bump_time:
            time_since_last_bump = datetime.now(timezone.utc) - self.last_bump_time
            if time_since_last_bump >= self.bump_interval:
                await channel.send("De server is klaar om gepusht te worden! Dit kan d.m.v het command `/bump`. Dit helpt de gezelligheid extra leven in te blazen.!")
                self.last_bump_time = datetime.now(timezone.utc)
        else:
            self.last_bump_time = datetime.now(timezone.utc)
            await self.send_to_log("De server is klaar om gepusht te worden! Dit kan d.m.v het command `/bump`. Dit helpt de gezelligheid extra leven in te blazen.!")

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_bump.start()

def setup(bot):
    bot.add_cog(BumpReminder(bot))