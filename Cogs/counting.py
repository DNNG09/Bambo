import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.InteractionBot(intents=disnake.Intents.all())

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv('COUNTING'))
        self.last_number = 0
        self.last_user_id = None

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("Channel not found!")
            return

        async for message in channel.history(limit=50):
            try:
                number = int(message.content.strip())
            except ValueError:
                continue

            self.last_number = number
            self.last_user_id = message.author.id
            break
        print(f"Counting cog is ready. Last number: {self.last_number}, Last user ID: {self.last_user_id}")
        await channel.send(f"🔢 Counting game is back online! Laatste getal was: **{self.last_number}**")

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        if message.channel.id != self.channel_id:
            return

        try:
            number = int(message.content.strip())
        except ValueError:
            return

        if message.author.id == self.last_user_id:
            await message.add_reaction("❌")
            await message.reply("❌ Je kunt niet twee keer achter elkaar tellen!\n🔁 De telling is gereset.")
            self.last_number = 0
            self.last_user_id = None
            return

        if number == 69:
            await message.add_reaction("🍆")

        if number == 420:
            await message.add_reaction("🌿")
        
        if number == 666:
            await message.add_reaction("😈")

        if number == 777:
            await message.add_reaction("☘️")
        
        if number == 1337:
            await message.add_reaction("💻")

        if number == 1234:
            await message.add_reaction("🔢")

        if number == 911:
            await message.add_reaction("✈️")
            await message.add_reaction("🏨")

        if number != self.last_number + 1:
            await message.add_reaction("❌")
            await message.reply(f"❌ Verkeerd getal! Het volgende juiste nummer was **{self.last_number + 1}**.\n🔁 De telling is gereset.")
            self.last_number = 0
            self.last_user_id = None
            return

        # Alles is correct
        self.last_number = number
        self.last_user_id = message.author.id
        await message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Counting(bot))
