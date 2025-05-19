import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

bot = commands.Bot(intents=disnake.Intents.all())
intents = disnake.Intents.default()
intents.messages = True

load_dotenv()

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Message Cog is loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: 
            return

        print(f"Message from {message.author}: {message.content}")

        invites = ["invite", "invitelink", "uitnodiging", "uitnodigingslink"]
        
        for i in invites:
            if i in (message.content).lower():
                await message.reply("Are you looking for the invite link to this server?")
                await message.reply(f"The link to this server is: {os.getenv('invite')}")


def setup(bot):
    bot.add_cog(Messages(bot))