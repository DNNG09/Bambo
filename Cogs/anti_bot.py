import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(intents=disnake.Intents.all())
intents = disnake.Intents.default()
intents.messages = True

class AntiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_to_kick_id = os.getenv('anti_bot')
        print("Anti Bot Cog is loaded")

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        added_roles = [role for role in after.roles if role not in before.roles]

        for role in added_roles:
            if role.id == self.role_to_kick_id:
                try:
                    await after.kick(reason=f"Received forbidden role: {role.name}")
                    print(f"Kicked {after} for receiving role {role.name}")
                except disnake.Forbidden:
                    print(f"Missing permissions to kick {after}.")
                except Exception as e:
                    print(f"Error kicking {after}: {e}")

def setup(bot):
    bot.add_cog(AntiBot(bot))