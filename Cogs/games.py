import disnake
from disnake.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Games Cog is geladen")

    @commands.slash_command(name="roll", description="Rol een dobbelsteen tussen 1 en 100")
    async def roll(self, inter: disnake.ApplicationCommandInteraction):
        result = random.randint(1, 100)
        await inter.response.send_message(f"🎲 Je rolde een **{result}**!")

    @commands.slash_command(name="wouldyourather", description="Zou je liever...? vraag")
    async def would_you_rather(self, inter: disnake.ApplicationCommandInteraction):
        options = [
            ("Vliegen als een vogel", "Onzichtbaar zijn"),
            ("Altijd de waarheid moeten zeggen", "Altijd moeten liegen"),
            ("Nooit meer internet", "Nooit meer muziek"),
            ("In het verleden reizen", "In de toekomst reizen"),
            ("Altijd kunnen teleporteren", "Altijd kunnen vliegen"),
            ("Nooit meer slapen", "Nooit meer eten"),
            ("Een jaar zonder telefoon", "Een jaar zonder vrienden zien"),
            ("Altijd koud hebben", "Altijd warm hebben"),
            ("Kunnen lezen gedachten", "Kunnen stoppen de tijd"),
            ("Nooit meer kunnen lachen", "Nooit meer kunnen huilen"),
            ("Nooit meer chocola eten", "Nooit meer pizza eten"),
            ("Altijd te laat zijn", "Altijd te vroeg zijn"),
            ("Leven in een wereld zonder kleuren", "Leven in een wereld zonder geluid"),
            ("Altijd je dromen onthouden", "Altijd je verleden vergeten"),
            ("Kunnen praten met dieren", "Kunnen praten met machines"),
            ("Iedereen kan je gedachten horen", "Je kan nooit meer iets zeggen"),
            ("Altijd natte sokken hebben", "Altijd een zandzak op je rug dragen"),
            ("Een miljoen euro winnen maar nooit gelukkig zijn", "Arm blijven maar gelukkig zijn"),
            ("Altijd op blote voeten lopen", "Altijd dikke schoenen dragen"),
            ("Altijd honger hebben", "Altijd dorst hebben"),
            ("Een jaar in isolatie zitten", "Een jaar in chaos leven"),
            ("Nooit meer muziek luisteren", "Nooit meer films kijken"),
            ("Altijd te veel praten", "Altijd te weinig zeggen"),
            ("Nooit meer vakantie", "Nooit meer weekend"),
            ("Je hele leven lang elke dag hetzelfde eten", "Je hele leven lang elke dag iets nieuws eten"),
            ("Een pauzeknop voor het leven hebben", "Een rewindknop voor het leven hebben"),
            ("Altijd perfect gekleed zijn", "Altijd perfect voorbereid zijn"),
            ("Je naam vergeten", "De namen van anderen vergeten"),
            ("Altijd vastzitten in een file", "Altijd vliegen met vertraging"),
            ("Je favoriete muziek nooit meer horen", "Nooit meer een nieuw liedje ontdekken"),
            ("Elke dag 10 kilometer lopen", "Elke dag 10 kilometer zwemmen"),
            ("Altijd in het donker leven", "Altijd in fel licht leven"),
            ("Altijd de weg weten", "Altijd de juiste keuze maken"),
            ("Nooit meer social media", "Nooit meer tv kijken"),
            ("Altijd te veel geld uitgeven", "Altijd te weinig geld hebben"),
            ("Je hele leven met een bril lopen", "Je hele leven lenzen dragen"),
            ("Een dier kunnen zijn naar keuze", "Een superheld kunnen zijn"),
            ("Nooit meer je huis verlaten", "Nooit meer terug kunnen naar huis"),
            ("Elke dag een verrassing", "Altijd weten wat er gaat gebeuren"),
            ("Een dag kunnen leven zonder herinneringen", "Een dag kunnen leven zonder emoties"),
            ("Onzichtbaar zijn voor iedereen", "Onhoorbaar zijn voor iedereen"),
            ("Een taal kunnen spreken die niemand anders spreekt", "Iedere taal kunnen verstaan maar niet spreken"),
            ("Je leeftijd nooit veranderen", "Je gewicht nooit veranderen"),
            ("Voor altijd jong blijven", "Voor altijd wijs blijven"),
            ("Altijd blij zijn", "Altijd kalm blijven"),
            ("De toekomst kunnen voorspellen", "De gedachten van anderen kunnen lezen"),
            ("Nooit meer hoeven slapen", "Nooit meer hoeven eten"),
            ("Een maand zonder internet", "Een maand zonder je beste vriend(in) zien"),
            ("Je leven kunnen resetten", "Je leven kunnen pauzeren"),
            ("Altijd 10 minuten te vroeg zijn", "Altijd 10 minuten te laat zijn"),
            ("Je hele leven in één stad wonen", "Elke maand verhuizen naar een nieuwe plek"),
            ("Altijd je droomjob hebben", "Altijd genoeg geld hebben"),
            ("Altijd eerlijk zijn", "Altijd aardig zijn"),
            ("Je grootste angst onder ogen komen", "Je grootste wens nooit bereiken"),
            ("Een dag leven zonder technologie", "Een dag leven zonder mensen"),
            ("Nooit meer kunnen reizen", "Nooit meer nieuwe mensen ontmoeten"),
            ("Elke dag kunnen koken als een topchef", "Elke dag kunnen zingen als een professionele zanger"),
            ("Nooit meer sporten", "Nooit meer junkfood eten"),
            ("De wereld kunnen veranderen", "Onsterfelijk zijn"),
            ("Altijd een goed humeur hebben", "Altijd energiek zijn"),
            ("Nooit meer stress hebben", "Nooit meer moe zijn"),
            ("Altijd het juiste antwoord weten", "Altijd het juiste gevoel hebben"),
            ("Een dag kunnen leven als een beroemdheid", "Een dag kunnen leven als een onbekende held"),
            ("Elke dag een nieuwe taal leren", "Elke dag een nieuw instrument leren bespelen"),
            ("Altijd kunnen dansen", "Altijd kunnen tekenen"),
            ("Je verleden kunnen wissen", "Je toekomst kunnen veranderen"),
            ("Elke dag een verrassingsfeest", "Elke dag een moment voor jezelf"),
            ("Altijd een goed boek vinden om te lezen", "Altijd een goede film vinden om te kijken"),
            ("Nooit meer koud hebben", "Nooit meer warm hebben"),
            ("Kunnen vliegen, maar nooit landen", "Kunnen lopen, maar nooit rennen"),
            ("Een dag leven als een dier", "Een dag leven als een robot"),
            ("Altijd een grappige opmerking hebben", "Altijd een wijze raad geven"),
            ("Nooit meer ruzie maken", "Nooit meer verdriet hebben"),
            ("Een tijdmachine hebben", "Een teleportatiemachine hebben"),
            ("Een onzichtbare cape hebben", "Een magische spreuk beheersen"),
            ("Elke dag gratis eten krijgen", "Elke dag gratis kleding krijgen"),
            ("Nooit meer hoofdpijn hebben", "Nooit meer moe zijn"),
            ("Je beste vriend(in) kunnen veranderen in een superheld", "Je grootste vijand kunnen veranderen in een vriend"),
            ("Altijd kunnen slapen wanneer je wilt", "Altijd kunnen eten wat je wilt"),
            ("Een geheime identiteit hebben", "Open en eerlijk zijn over alles"),
            ("Je eigen eiland bezitten", "Een luxe penthouse in de stad hebben"),
            ("Nooit meer moeten werken", "Nooit meer geldzorgen hebben"),
            ("Kunnen spreken met dieren", "Kunnen spreken met buitenaardse wezens"),
            ("Nooit meer alleen zijn", "Nooit meer iemand teleurstellen"),
            ("Altijd op avontuur zijn", "Altijd thuis kunnen komen"),
            ("De perfecte vakantie elke keer", "Altijd het perfecte cadeau geven"),
            ("Iedereen kunnen laten lachen", "Iedereen kunnen troosten"),
            ("Nooit meer ziek zijn", "Nooit meer ongelukkig zijn"),
        ]

        vraag = random.choice(options)
        await inter.response.send_message(f"🤔 Zou je liever **{vraag[0]}** of **{vraag[1]}**?")

    @commands.slash_command(name="roll", description="Rol een dobbelsteen tussen 1 en 100")
    async def roll(self, inter: disnake.ApplicationCommandInteraction):
        result = random.randint(1, 100)
        await inter.response.send_message(f"🎲 Je rolde een **{result}**!")

    @commands.slash_command(name="wouldyourather", description="Zou je liever...? vraag")
    async def would_you_rather(self, inter: disnake.ApplicationCommandInteraction):
        options = [
            ("Vliegen als een vogel", "Onzichtbaar zijn"),
            ("Altijd de waarheid moeten zeggen", "Altijd moeten liegen"),
            ("Nooit meer internet", "Nooit meer muziek"),
            ("In het verleden reizen", "In de toekomst reizen")
        ]
        vraag = random.choice(options)
        await inter.response.send_message(f"🤔 Zou je liever **{vraag[0]}** of **{vraag[1]}**?")

    @commands.slash_command(name="truthordare", description="Waarheid of durven")
    async def truth_or_dare(self, inter: disnake.ApplicationCommandInteraction):
        truths = [
            "Wat is je grootste geheim?",
            "Wie vind je stiekem leuk?",
            "Wat is het meest gênante wat je ooit hebt gedaan?",
            "Wat is je vreemdste gewoonte?",
            "Wat is het meest beschamende moment uit je leven?",
            "Heb je ooit iemand verraden?",
            "Wat zou je doen als je onzichtbaar was voor een dag?",
            "Wat is het raarste wat je ooit hebt gegeten?",
            "Ben je ooit verliefd geweest op een leraar?",
            "Wat is het ergste wat je ooit tegen iemand hebt gezegd?",
            "Wat is je grootste angst?",
            "Wat is de grootste leugen die je ooit hebt verteld?",
            "Wat is het domste dat je ooit hebt gedaan?",
            "Wat is je meest beschamende schoolmoment?",
            "Wat zou je doen met een miljoen euro?",
            "Heb je ooit iets gestolen?",
            "Wie was je eerste crush?",
            "Wat is je slechtste eigenschap?",
            "Waar schaam je je het meest voor?",
            "Wat is je vreemdste droom ooit?",
            "Heb je ooit gedaan alsof je iemand leuk vond?",
            "Wat is het stomste wat je in een ruzie hebt gezegd?",
            "Wat zou je doen als je een dag van geslacht kon veranderen?",
            "Wie is je geheime idool?",
            "Wat is iets dat bijna niemand over jou weet?",
            "Wat is de meest beschamende muziek die je leuk vindt?",
            "Heb je ooit gefaald voor iets belangrijks?",
            "Wat is je grootste spijt?",
            "Wat zou je doen als niemand je ooit zou beoordelen?",
            "Wie zou je bellen als je in de gevangenis zat?",
            "Wat zou je doen als je de loterij won?",
            "Wat is je vreemdste jeugdherinnering?",
            "Heb je ooit iets kapotgemaakt en het niet verteld?",
            "Wat is het stomste dat je ooit hebt geloofd?",
            "Wat is het gekste dat je ooit hebt gedaan uit liefde?",
            "Wat is het gemeenste wat je ooit hebt gedaan?",
            "Wat zou je absoluut nooit doen, zelfs niet voor geld?",
            "Wat is je grootste verslaving?",
            "Wat is iets wat je altijd al hebt willen proberen?",
            "Heb je ooit gelogen tegen een vriend(in)?",
            "Wat is je vreemdste fantasie?",
        ]

        dares = [
            "Doe 10 jumping jacks voor de camera!",
            "Zing een stukje van een bekend liedje.",
            "Vertel een mop of grappig verhaal.",
            "Trek een gek gezicht en maak een selfie.",
            "Praat 1 minuut in een raar accent.",
            "Doe alsof je een kip bent voor 30 seconden.",
            "Laat je laatste zoekopdracht op Google zien.",
            "Eet een lepel mosterd.",
            "Dans zonder muziek voor 30 seconden.",
            "Laat de inhoud van je tas of broekzak zien.",
            "Bel iemand en zing 'Happy Birthday'.",
            "Post een gênante foto van jezelf in een kanaal.",
            "Verander je nickname voor 1 uur in iets belachelijks.",
            "Eet een rauw ei (alleen als veilig).",
            "Probeer je elleboog te likken en laat het zien.",
            "Typ 1 minuut lang met je neus.",
            "Doe een nep-lach voor 30 seconden.",
            "Zeg het alfabet achterstevoren.",
            "Zeg 5 complimenten tegen jezelf hardop.",
            "Trek 3 kledingstukken over elkaar aan en laat ze zien.",
            "Neem een gek stemmetje op en stuur het in een kanaal.",
            "Lees een bericht voor alsof je in een soap speelt.",
            "Doe een dansje alsof je op TikTok bent.",
            "Eet een stukje citroen zonder een gezicht te trekken.",
            "Spreek een liefdesverklaring in aan een willekeurig object.",
            "Vertel het weerbericht op een dramatische manier.",
            "Zeg 'ik ben een banaan' 10 keer op verschillende manieren.",
            "Houd je adem 20 seconden in en doe dan alsof je verbaasd bent.",
            "Maak een dierengeluid en laat mensen raden welk dier het is.",
            "Doe alsof je een nieuwslezer bent en breng breaking news."
        ]

        keuze = random.choice(["waarheid", "durven"])
        if keuze == "waarheid":
            vraag = random.choice(truths)
            await inter.response.send_message(f"🗣 Waarheid: {vraag}")
        else:
            opdracht = random.choice(dares)
            await inter.response.send_message(f"🎯 Durven: {opdracht}")


def setup(bot):
    bot.add_cog(Games(bot))
