import os
from disnake.ext import commands
import disnake
from dotenv import load_dotenv

load_dotenv()  

client = commands.InteractionBot(intents=disnake.Intents.all())
bot = commands.InteractionBot(intents=disnake.Intents.all())

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Welcome Cog is loaded!")

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        guild_name = guild.name

        welcome_channel = disnake.utils.get(guild.WELCOME_CHANNELS, name="welcome")

        rules_channel = os.getenv("RULES", "#regels")
        intro_channel = os.getenv("INTRODUCE", "#voorstellen")
        anouncements_channel = os.getenv("ANNOUNCEMENTS", "#aankondigingen")
        tickets = os.getenv("TICKETS", "#tickets")

        if welcome_channel:
            await welcome_channel.send(
                f"👋 Welkom {member.mention} in **{guild_name}**!\n\n"
                "Deze server is een **veilige haven voor iedereen** waar, ondanks dat de humor soms een beetje het randje opzoekt **respect voor elkaar** voorop staat. \n\n"
                "🎮 **Opgericht door DNNG en GamingPandaMommy**, maar gebouwd op de basis van een echte community:\n"
                "We zijn een diverse groep mensen die van gamen, memes, en gewoon gezellig kletsen houden. Of je nu een gamer bent, een meme-liefhebber, of gewoon iemand die graag nieuwe vrienden maakt, je bent hier op de juiste plek!\n\n"
                "Iedereen is welkom, en we hopen dat je je hier snel thuis voelt!\n\n"
                
                "🔎 Hier zijn een paar dingen die je moet weten:\n"
                
                f"1️⃣ **Lees de 📜 regels** in het kanaal {rules_channel}.\n"
                f"2️⃣ **Stel jezelf voor** in het kanaal {intro_channel}.\n"
                f"3️⃣ **Check de 📢 {anouncements_channel}** voor belangrijke updates en evenementen.\n\n"
                
                "🤖 We hebben ook een aantal leuke bots en functies die je kunt ontdekken, dus voel je vrij om rond te kijken!\n\n"

                f"❓ Als je vragen hebt, stel ze gerust in {tickets} of stuur een DM naar een van de moderators.\n\n"

                "Fijn dat je er bent! We kijken ernaar uit om je te leren kennen! 💬"
            )


def setup(bot):
    bot.add_cog(Welcome(bot))