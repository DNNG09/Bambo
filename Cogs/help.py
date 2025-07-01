import disnake
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Help Cog is loaded")

    @commands.slash_command(
        name="help",
        description="Toon een lijst met beschikbare commando's, netjes per categorie."
    )
    async def help_command(self, inter: disnake.ApplicationCommandInteraction):  # <-- self toegevoegd
        embed = disnake.Embed(
            title="📘 Bambo Help",
            description="Hieronder vind je alle beschikbare slash-commando's, gesorteerd per categorie:",
            color=disnake.Color.blurple()
        )

        embed.add_field(
            name="🎉 Fun & Spelletjes",
            value="\n".join([
                "`/roll` – Rol een dobbelsteen (bijv. d20)",
                "`/wouldyourather` – Zou je liever…?",
                "`/truthordare` – Waarheid of durven",
                "`/hug [gebruiker]` – Geef een knuffel",
                "`/highfive [gebruiker]` – High five!",
                "`/boop [gebruiker]` – Boop iemands neus",
                "`/compliment [gebruiker]` – Geef een compliment",
                "`/insult [gebruiker]` – Semi-lieve roast"
            ]),
            inline=False
        )

        embed.add_field(
            name="📊 Polls & Stemmen",
            value="\n".join([
                "`/poll` – Start een poll met meerdere opties"
            ]),
            inline=False
        )

        embed.add_field(
            name="🎮 Community & Tools",
            value="\n".join([
                "`/ticket` – Open een supportticket",
                "`/ping` – Check of de bot leeft",
                "`/info` – Info over de server & founders",
                "`/regels` – Toon de serverregels",
                "`/staff` – Lijst met staffleden"
            ]),
            inline=False
        )

        embed.set_footer(text="Gebruik / gevolgd door het commando, bijvoorbeeld: /poll")
        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))
