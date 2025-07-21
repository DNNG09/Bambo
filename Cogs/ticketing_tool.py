import disnake
from disnake.ext import commands
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("GUILD_ID"))
TICKET_CATEGORY_ID = str(os.getenv("TICKET_CATEGORY_ID"))
SUPPORT_ROLE_ID = int(os.getenv("SUPPORT_ROLE_ID"))
TICKET_LOG_CHANNEL_ID = int(os.getenv("TICKET_LOG_CHANNEL_ID"))


class TicketView(disnake.ui.View):
    def __init__(self, reason, author):
        super().__init__(timeout=None)
        self.reason = reason
        self.author = author

    @disnake.ui.button(label="Sluit Ticket", style=disnake.ButtonStyle.danger, emoji="🔒")
    async def close_ticket(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.channel and interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message(
                "Weet je zeker dat je dit ticket wilt sluiten?",
                view=ConfirmCloseView(interaction.channel, self.author),
                ephemeral=True
            )


class ConfirmCloseView(disnake.ui.View):
    def __init__(self, channel, author):
        super().__init__(timeout=60)
        self.channel = channel
        self.author = author

    @disnake.ui.button(label="Ja, sluiten", style=disnake.ButtonStyle.danger)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        # Samenvatting ophalen
        messages = await self.channel.history(limit=100).flatten()
        messages.reverse()
        transcript = ""
        for msg in messages:
            timestamp = msg.created_at.strftime("%H:%M")
            transcript += f"[{timestamp}] {msg.author.name}: {msg.content}\n"

        embed = disnake.Embed(
            title="🎫 Ticket Gesloten",
            description=f"Samenvatting van je ticket **{self.channel.name}**",
            color=disnake.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Reden", value=self.channel.topic or "Onbekend", inline=False)
        embed.add_field(name="Samenvatting (laatste 100 berichten)", value=transcript[:1000] or "*Geen berichten*", inline=False)

        try:
            await self.author.send(embed=embed)
        except:
            pass  # DM niet gelukt

        log_channel = interaction.guild.get_channel(TICKET_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"📁 Ticket gesloten: {self.channel.name} door {interaction.user.mention}")

        await self.channel.delete()

    @disnake.ui.button(label="Nee, annuleren", style=disnake.ButtonStyle.secondary)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Ticket sluiten geannuleerd.", ephemeral=True)


class TicketingTool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✅ TicketingTool geladen")

    @commands.slash_command(description="Open een nieuw support ticket.")
    async def ticket(self, inter: disnake.AppCmdInter, reden: str = commands.Param(description="Geef een korte omschrijving van je probleem")):
        await inter.response.defer(ephemeral=True)

        guild = inter.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        support_role = guild.get_role(SUPPORT_ROLE_ID)

        existing = disnake.utils.get(guild.text_channels, name=f"ticket-{inter.author.name.lower()}")
        if existing:
            await inter.send("Je hebt al een open ticket.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            inter.author: disnake.PermissionOverwrite(view_channel=True, send_messages=True),
            support_role: disnake.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{inter.author.name}",
            topic=reden,
            category=category,
            overwrites=overwrites
        )

        embed = disnake.Embed(
            title="🎟️ Nieuw Ticket",
            description=f"{inter.author.mention} heeft een ticket geopend.\n**Reden:** {reden}",
            color=disnake.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        await channel.send(embed=embed, view=TicketView(reden, inter.author))
        await inter.send(f"✅ Ticket aangemaakt: {channel.mention}", ephemeral=True)

    @commands.slash_command(description="Sluit dit ticket.")
    async def ticket_close(self, inter: disnake.AppCmdInter):
        if not inter.channel.name.startswith("ticket-"):
            await inter.response.send_message("⛔ Dit is geen ticketkanaal.", ephemeral=True)
            return

        await inter.response.send_message(
            "Weet je zeker dat je dit ticket wilt sluiten?",
            view=ConfirmCloseView(inter.channel, inter.author),
            ephemeral=True
        )

    @commands.slash_command(description="Voeg een gebruiker toe aan dit ticket.")
    async def ticket_adduser(self, inter: disnake.AppCmdInter, gebruiker: disnake.Member):
        if not inter.channel.name.startswith("ticket-"):
            await inter.response.send_message("⛔ Dit is geen ticketkanaal.", ephemeral=True)
            return

        await inter.channel.set_permissions(gebruiker, view_channel=True, send_messages=True)
        await inter.response.send_message(f"✅ {gebruiker.mention} is toegevoegd aan dit ticket.", ephemeral=True)

    @commands.slash_command(description="Verwijder een gebruiker uit dit ticket.")
    async def ticket_removeuser(self, inter: disnake.AppCmdInter, gebruiker: disnake.Member):
        if not inter.channel.name.startswith("ticket-"):
            await inter.response.send_message("⛔ Dit is geen ticketkanaal.", ephemeral=True)
            return

        await inter.channel.set_permissions(gebruiker, overwrite=None)
        await inter.response.send_message(f"❌ {gebruiker.mention} is verwijderd uit dit ticket.", ephemeral=True)

    @commands.slash_command(description="Hernoem dit ticketkanaal.")
    async def ticket_rename(self, inter: disnake.AppCmdInter, nieuwe_naam: str):
        if not inter.channel.name.startswith("ticket-"):
            await inter.response.send_message("⛔ Dit is geen ticketkanaal.", ephemeral=True)
            return

        await inter.channel.edit(name=f"ticket-{nieuwe_naam}")
        await inter.response.send_message(f"🔁 Kanaal hernoemd naar `ticket-{nieuwe_naam}`", ephemeral=True)

    @commands.slash_command(description="Pas de reden van het ticket aan.")
    async def ticket_topic(self, inter: disnake.AppCmdInter, reden: str):
        if not inter.channel.name.startswith("ticket-"):
            await inter.response.send_message("⛔ Dit is geen ticketkanaal.", ephemeral=True)
            return

        await inter.channel.edit(topic=reden)
        await inter.response.send_message(f"📝 Reden aangepast naar:\n> {reden}", ephemeral=True)


def setup(bot):
    bot.add_cog(TicketingTool(bot))
