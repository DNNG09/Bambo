import disnake
from disnake.ext import commands, tasks
import os
import datetime
import requests

class YouTubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
        self.discord_channel_id = int(os.getenv("DISCORD_NOTIFY_CHANNEL"))
        self.last_live_video_id = None
        self.check_youtube_live.start()

    def is_live(self):
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet"
            f"&channelId={self.channel_id}"
            f"&eventType=live"
            f"&type=video"
            f"&key={self.api_key}"
        )
        response = requests.get(url).json()
        items = response.get("items", [])
        return items[0] if items else None

    @tasks.loop(minutes=1)
    async def check_youtube_live(self):
        video = self.is_live()
        if video:
            video_id = video['id']['videoId']
            if self.last_live_video_id != video_id:
                self.last_live_video_id = video_id
                url = f"https://www.youtube.com/watch?v={video_id}"
                title = video['snippet']['title'],
                description = f"{os.getenv('LIVE_MELDING')}: Kom gezellig meedoen!"
                thumbnail = video['snippet']['thumbnails']['high']['url']

                embed = disnake.Embed(
                    title=f"🎥 {os.getenv('DEVELOPER')} is LIVE! op YouTube!",
                    description=f"[{title}]({url})",
                    color=disnake.Color.red(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_thumbnail(url=thumbnail)
                embed.set_footer(text="YouTube Live Notificatie")

                channel = self.bot.get_channel(self.discord_channel_id)
                if channel:
                    await channel.send(embed=embed)
        else:
            self.last_live_video_id = None  # Reset als je offline bent

    @check_youtube_live.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    @commands.slash_command(description="Check of DNNG live is op YouTube")
    async def livestatus(self, inter: disnake.AppCmdInter):
        await inter.response.defer()
        video = self.is_live()
        if video:
            video_id = video['id']['videoId']
            url = f"https://www.youtube.com/watch?v={video_id}"
            await inter.send(f"✅ Je bent live: {url}")
        else:
            await inter.send("🔴 Je favoriete Pandasaurus Rex is op dit moment niet live.")
            await inter.send(f"Je kunt de laatste video bekijken op: https://www.youtube.com/channel/{os.getenv('YOUTUBE_CHANNEL_ID')}/videos")

def setup(bot):
    bot.add_cog(YouTubeCog(bot))
