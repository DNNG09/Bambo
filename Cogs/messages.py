import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

client = commands.InteractionBot(intents=disnake.Intents.all())
bot = commands.InteractionBot(intents=disnake.Intents.all())

load_dotenv()

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Message Cog is loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: 
            return

        #print(f"Message from {message.author}: {message.content}")

        invites = ["invite", "invitelink", "uitnodiging", "uitnodigingslink"]
        invite = os.getenv('INVITE_LINK')
        
        for i in invites:
            if i in (message.content).lower():
                await message.reply("Leuk dat je de gezelligheid nog groter wilt maken! Hier is de link naar deze server:")
                await message.reply(f"The link to this server is: {invite}")


def setup(bot):
    bot.add_cog(Messages(bot))