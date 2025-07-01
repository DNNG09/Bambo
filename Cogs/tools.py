import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions
import datetime
import time
import random
import asyncio

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        print("Tools Cog is geladen")

    mod_roles = 1326151023974154260


    @commands.slash_command(name="ping", description="Check of de bot online is en zie de latency.")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        latency = round(self.bot.latency * 1000)  # in ms
        await inter.response.send_message(f"Pong! 🏓 Latency: {latency} ms")

    @has_permissions(administrator=True)
    @commands.slash_command(name="userinfo", description="Toon informatie over een gebruiker.")
    async def userinfo(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member = None):
        user = user or inter.user
        embed = disnake.Embed(title=f"Info over {user}", color=disnake.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Gebruikersnaam", value=str(user), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Account gemaakt op", value=user.created_at.strftime("%d-%m-%Y %H:%M"), inline=False)
        embed.add_field(name="Lid sinds", value=user.joined_at.strftime("%d-%m-%Y %H:%M") if user.joined_at else "Onbekend", inline=False)
        embed.add_field(name="Bot?", value="Ja" if user.bot else "Nee", inline=True)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="serverinfo", description="Toon informatie over de server.")
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild
        embed = disnake.Embed(title=f"Info over {guild.name}", color=disnake.Color.green())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Eigenaar", value=str(guild.owner), inline=True)
        embed.add_field(name="Aantal leden", value=guild.member_count, inline=True)
        embed.add_field(name="Aantal kanalen", value=len(guild.channels), inline=True)
        embed.add_field(name="Gemaakt op", value=guild.created_at.strftime("%d-%m-%Y %H:%M"), inline=False)
        await inter.response.send_message(embed=embed)

    @has_permissions(administrator=True)
    @commands.slash_command(name="avatar", description="Toon de profielfoto van een gebruiker.")
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member = None):
        user = user or inter.user
        embed = disnake.Embed(title=f"Avatar van {user}", color=disnake.Color.blurple())
        embed.set_image(url=user.display_avatar.url)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="uptime", description="Toon hoe lang de bot online is.")
    async def uptime(self, inter: disnake.ApplicationCommandInteraction):
        uptime_seconds = int(time.time() - self.start_time)
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
        await inter.response.send_message(f"De bot is al {uptime_str} online.")

    @commands.slash_command(name="food", description="Welk fastfood Restaurant word het vandaag?")
    async def food(self, inter: disnake.ApplicationCommandInteraction):
        restaurants = [
            "McDonald's",
            "Burger King",
            "KFC",
            "Subway",
            "Domino's Pizza",
            "New York Pizza",
        ]
        await inter.response.send_message(f"Vandaag gaan we naar {random.choice(restaurants)}!")

    
    @commands.slash_command(name="remind", description="Stel een herinnering in in minuten.")
    async def remind(self, inter: disnake.ApplicationCommandInteraction, tijd: int, *, bericht: str):
        await inter.response.send_message(f"✅ Ik herinner je over {tijd} minuut(en): {bericht}", ephemeral=True)
        await asyncio.sleep(tijd * 60)
        await inter.followup.send(f"⏰ Herinnering: {bericht}", user=inter.user)

    @commands.slash_command(name="8ball", description="Stel een ja/nee vraag en krijg een antwoord.")
    async def eight_ball(self, inter: disnake.ApplicationCommandInteraction, vraag: str):
        antwoorden = [
            "Ja", "Nee", "Misschien", "Zeker weten", "Ik weet het niet",
            "Vraag later nog eens", "Absoluut", "Niet echt", "Zonder twijfel"
        ]
        await inter.response.send_message(f"🎱 Vraag: {vraag}\nAntwoord: {random.choice(antwoorden)}")
    
    @commands.slash_command(name="choose", description="Laat de bot een keuze maken tussen meerdere opties.")
    async def choose(self, inter: disnake.ApplicationCommandInteraction, *keuzes: str):
        if not keuzes: 
            await inter.response.send_message("Je moet ten minste één keuze opgeven.", ephemeral=True)
            return
        keuze = random.choice(keuzes)
        await inter.response.send_message(f"De bot kiest: {keuze}")

    @commands.slash_command(name="coinflip", description="Gooi een munt op: kop of munt?")
    async def coinflip(self, inter: disnake.ApplicationCommandInteraction):
        result = random.choice(["Kop", "Munt"])
        await inter.response.send_message(f"De munt valt op **{result}**!")



def setup(bot):
    bot.add_cog(Tools(bot))
