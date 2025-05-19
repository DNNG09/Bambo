import disnake
import requests
from disnake.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
import logging
from datetime import datetime

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.qotd_channel_id = os.getenv('qotd')
        self.qotd_channel = None
        print("QOTD Cog is loaded!")

        
    today = datetime.today()
    current_time = today.strftime("%H:%M")

    questions = [
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


    @tasks.loop(minutes=1)
    async def qotd_loop(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == "19:45" and now.date() != self.sent_today:
            question = random.choice(self.questions)
            channel = self.bot.get_channel(self.qotd_channel_id)
            if channel:
                await channel.send(f"📢 **Vraag van de dag:**\n{question}")
                self.sent_today = now.date()
            else:
                print("Kanaal niet gevonden voor QOTD.")

    @qotd_loop.before_loop
    async def before_qotd_loop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(QOTD(bot))