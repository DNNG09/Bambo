import disnake
from disnake.ext import commands, tasks
import os
import random
from datetime import datetime
from dotenv import load_dotenv

bot = commands.InteractionBot(intents=disnake.Intents.all())
intents = disnake.Intents.default()
intents.messages = True

class StatementOfTheDay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
        load_dotenv()

        self.sotd_channel_id = os.getenv('SOTD_CHANNEL_ID')  # bijv. 123456789012345678
        self.sent_today = None  # om dubbele berichten te voorkomen
        self.send_message.start()
        self.sotd_loop.start()

        print("StatementOfTheDay Cog is loaded!")


    statements = [
            "Geluk is een keuze.",
            "Moet iedereen verantwoordelijk zijn voor zijn eigen geluk, of heeft de samenleving hier ook een rol in?",
            "Kun je pas echt gelukkig zijn als je anderen gelukkig maakt?",
            "Is geluk afhankelijk van je mindset of van je omstandigheden?",
            "Bestaat er zoiets als objectief geluk?",
            "Moeten scholen kinderen leren hoe ze gelukkig kunnen zijn?",
            "Iedereen verdient een tweede kans.",
            "Je kunt niet voor een ander zorgen als je niet voor jezelf zorgt.",
            "Ziekenhuizen moeten meer investeren in preventie.",
            "Elke school moet een verplichte stilteklas hebben.",
            "Vlees eten moet sterk worden ontmoedigd.",
            "Boetes zouden inkomensafhankelijk moeten zijn.",
            "Kinderen onder de 12 zouden geen smartphone mogen hebben.",
            "Rijke mensen moeten meer belasting betalen.",
            "Falen is noodzakelijk om te groeien.",
            "TikTok moet verboden worden in Europa.",
            "Politiek moet dichter bij de burger staan.",
            "Religie hoort thuis in het publieke debat.",
            "Tijd is waardevoller dan geld.",
            "Minimalisme maakt het leven beter.",
            "Werken om te leven is beter dan leven om te werken.",
            "Schooluniformen zouden verplicht moeten zijn.",
            "Iedereen moet jaarlijks verplicht een psychologische check-up doen.",
            "Ouders moeten een opvoedcursus volgen.",
            "Je bent zelf verantwoordelijk voor je geluk.",
            "Studeren moet volledig gratis zijn.",
            "Sollicitatiebrieven zijn achterhaald.",
            "Iedereen moet vier dagen per week werken.",
            "Klimaatverandering is de grootste dreiging van onze tijd.",
            "Dieren hebben dezelfde rechten als mensen.",
            "Je mag geen cultuur toe-eigenen die niet van jou is.",
            "Fastfood moet extra belast worden.",
            "Democratie werkt alleen als burgers goed geïnformeerd zijn.",
            "Basisscholen moeten starten om 10:00 uur.",
            "Euthanasie moet voor iedereen mogelijk zijn.",
            "Robots moeten geen zorgfuncties vervullen.",
            "Mensen met zware beroepen moeten eerder met pensioen.",
            "Tradities mogen veranderen.",
            "Iedereen zou een basisinkomen moeten krijgen.",
            "Social media maakt mensen ongelukkiger.",
            "Je moet jezelf regelmatig opnieuw uitvinden.",
            "Het minimumloon is nog steeds te laag.",
            "Internettoegang is een mensenrecht.",
            "Vreemdgaan is een bewuste keuze, geen fout.",
            "Seksuele voorlichting moet vanaf groep 5 gegeven worden.",
            "Burn-outs worden niet serieus genoeg genomen.",
            "Je mag culturele gebruiken bekritiseren.",
            "Elke dag moet iets leren opleveren.",
            "Iedereen zou stemrecht moeten krijgen vanaf 16 jaar.",
            "Vrijheid van meningsuiting mag nooit beperkt worden.",
            "Deepfakes moeten strafbaar zijn.",
            "Zorgverzekeringen moeten standaard alternatieve geneeskunde vergoeden.",
            "Schoolkinderen moeten leren koken.",
            "Werknemers moeten recht hebben op thuiswerken.",
            "Thuiswerken moet een recht zijn.",
            "Elektrische auto's zijn niet de oplossing.",
            "Taal bepaalt je identiteit.",
            "Kunstmatige intelligentie vormt een bedreiging voor werkgelegenheid.",
            "Het leven zonder technologie zou beter zijn.",
            "Carnaval is belangrijker dan Koningsdag.",
            "Werkgevers moeten verantwoordelijk zijn voor de mentale gezondheid van werknemers.",
            "Anonieme donaties zijn minder ethisch dan transparante.",
            "Je bent niet verplicht om je ouders te verzorgen.",
            "Duurzaamheid moet een vak zijn op school.",
            "Zelfliefde is belangrijker dan romantische liefde.",
            "Schoolkinderen moeten meer buitenspelen dan naar school gaan.",
            "Burn-outs worden niet serieus genomen.",
            "Vliegen moet fors duurder worden.",
            "Robots moeten geen mensen vervangen in de zorg.",
            "Alcohol is schadelijker dan we denken.",
            "Ouderbetrokkenheid in het onderwijs gaat te ver.",
            "Kunst en cultuur moeten niet meer gesubsidieerd worden.",
            "Wraak kan gerechtvaardigd zijn.",
            "Iedereen heeft het recht om te falen.",
            "Technologie maakt ons luier.",
            "Lonen moeten transparant zijn binnen bedrijven.",
            "Internetanoniem zijn moet worden afgeschaft.",
            "De aarde heeft rust nodig van de mens.",
            "Dialecten moeten meer gewaardeerd worden.",
            "Plastic verpakkingen moeten worden verboden.",
            "Je moet altijd jezelf kunnen blijven.",
            "Minder spullen kopen is beter dan recyclen.",
            "Ouders bemoeien zich te veel met school.",
            "Kunstmatige intelligentie moet gereguleerd worden.",
            "Geld maakt gelukkig.",
            "Basisonderwijs moet meer op praktijk gericht zijn.",
            "Schoolkinderen moeten leren omgaan met stress.",
            "Sporten moet tijdens werktijd mogelijk zijn.",
            "Je hoeft niet altijd bereikbaar te zijn.",
            "Bedrijven moeten betalen voor hun CO₂-uitstoot.",
            "Vrijheid betekent ook verantwoordelijkheid nemen."
        ]


    @tasks.loop(seconds=60)
    async def send_message(self):
        channel = self.bot.get_channel(self.sotd_channel_id)
        if channel:
            return
        else:
            return

    @tasks.loop(seconds=5)
    async def sotd_loop(self):
        now = datetime.now()
        if now.strftime("%H:%M") == "18:00" and now.date() != self.sent_today:
            channel = self.bot.get_channel(self.sotd_channel_id)
            if channel:
                statement = random.choice(self.statements)
                await channel.send(f"📢 **Stelling van de dag:**\n{statement}")
                self.sent_today = now.date()


    @commands.slash_command(name="test_sotd", description="Stuur handmatig een stelling van de dag (alleen voor mods)")
    async def test_sotd(self, inter: disnake.ApplicationCommandInteraction):
        mod_role = disnake.utils.get(inter.guild.roles, name="ADMIN_1")  

        if mod_role in inter.author.roles:
            statement = random.choice(self.statements)
            await inter.response.send_message(f"📢 **Stelling van de dag (handmatig):**\n{statement}")
        else:
            await inter.response.send_message("⛔ Je hebt hier geen toestemming voor.", ephemeral=True)

def setup(bot):
    bot.add_cog(StatementOfTheDay(bot))