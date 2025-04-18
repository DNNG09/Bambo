import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_number = 0
        self.last_user_id = None
        self.channel_id =  os.getenv('counting')

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        if self.channel_id and message.channel.id != self.channel_id:
            return

        try:
            number = int(message.content.strip())
        except ValueError:
            return  

        if number == self.last_number + 1:
            await message.add_reaction("✅")
            self.last_number = number
            self.last_user_id = message.author.id
        else:
            await message.add_reaction("❌")
            await message.reply("This is not the correct number \nYou need to start all over again.")
            self.last_number = 0
            self.last_user_id = None



def setup(bot):
    bot.add_cog(Counting(bot))
