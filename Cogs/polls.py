# poll_cog.py
import os
import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions
from disnake.ui import View, Button, Select
import random
import logging

logger = logging.getLogger("polls")

active_polls = {}
mod_roles = 1326151023974154260

class PollButton(Button):
    def __init__(self, label: str, custom_id: str, emoji: str):
        super().__init__(
            label=label,
            custom_id=custom_id,
            emoji=emoji,
            style=disnake.ButtonStyle.blurple,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        view: "PollView" = self.view
        if view.vote(interaction.user.id, self.custom_id):
            await interaction.response.send_message(
                f"✅ Je stem voor **{self.custom_id}** is geregistreerd.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Je had al voor **{self.custom_id}** gestemd.",
                ephemeral=True,
            )


class PollDropdown(Select):
    def __init__(self, options: list[str]):
        select_options = [disnake.SelectOption(label=o, value=o) for o in options]
        super().__init__(
            placeholder="Kies een optie…",
            options=select_options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        view: "PollView" = self.view
        chosen = interaction.data["values"][0]
        if view.vote(interaction.user.id, chosen):
            await interaction.response.send_message(
                f"✅ Je stem voor **{chosen}** is geregistreerd.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Je had al voor **{chosen}** gestemd.",
                ephemeral=True,
            )


class PollView(View):
    def __init__(self, question: str, options: list[str], timeout: int, author_id: int):
        super().__init__(timeout=timeout)
        self.question = question
        self.options = options
        self.votes = {o: 0 for o in options}
        self.user_votes: dict[int, str] = {}
        self.author_id = author_id
        self.message: disnake.Message | None = None
        self.closed = False

        if len(options) <= 5:
            for idx, opt in enumerate(options):
                emoji = chr(0x1F1E6 + idx)  # 🇦  = U+1F1E6
                self.add_item(PollButton(opt, opt, emoji))
        else:
            self.add_item(PollDropdown(options))

    def vote(self, user_id: int, option: str) -> bool:
        """Geeft True als stem is toegevoegd/gewijzigd, False bij duplicaat."""
        if user_id in self.user_votes and self.user_votes[user_id] == option:
            return False  # dubbel

        previous = self.user_votes.get(user_id)
        if previous:
            self.votes[previous] -= 1
        self.user_votes[user_id] = option
        self.votes[option] += 1
        return True

    def results_str(self) -> str:
        total = sum(self.votes.values()) or 1
        lines = [
            f"**{opt}** — {v} stem(men) ({round(v / total * 100)}%)"
            for opt, v in self.votes.items()
        ]
        return "\n".join(lines)

    async def on_timeout(self):
        await self.close_poll()

    async def close_poll(self):
        if self.closed:
            return
        self.closed = True
        for child in self.children:
            child.disabled = True

        embed = disnake.Embed(
            title="📊 Pollresultaten",
            description=f"**{self.question}**\n\n{self.results_str()}",
            color=disnake.Color.green(),
        )
        await self.message.edit(embed=embed, view=self)
        active_polls.pop(self.message.guild.id, None)
        logger.info(
            "Poll closed in %s (%s) by timeout.",
            self.message.guild.name,
            self.message.guild.id,
        )

class Poll(commands.Cog):
    """Slash‑commands om polls te maken en resultaten op te vragen."""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        print("📊 Poll‑Cog geladen.")

    @commands.slash_command(
        name="poll",
        description="Maak een poll met 2‑10 opties (alleen voor mods).",
    )
    
    async def poll_create(
        self,
        inter: disnake.ApplicationCommandInteraction,
        vraag: str = commands.Param(name="vraag", description="De pollvraag"),
        duur: int = commands.Param(
            ge=1, le=60, name="duur", description="Duur in minuten (1‑60)"
        ),
        optie1: str = commands.Param(name="optie1"),
        optie2: str = commands.Param(name="optie2"),
        optie3: str | None = None,
        optie4: str | None = None,
        optie5: str | None = None,
        optie6: str | None = None,
        optie7: str | None = None,
        optie8: str | None = None,
        optie9: str | None = None,
        optie10: str | None = None,
    ):

        opts = [
            o
            for o in [
                optie1,
                optie2,
                optie3,
                optie4,
                optie5,
                optie6,
                optie7,
                optie8,
                optie9,
                optie10,
            ]
            if o
        ]
        if len(opts) < 2:
            await inter.response.send_message(
                "⚠️ Je moet minstens 2 opties opgeven.", ephemeral=True
            )
            return

        if inter.guild.id in active_polls:
            await inter.response.send_message(
                "⚠️ Er is al een actieve poll in deze server.",
                ephemeral=True,
            )
            return


        timeout_secs = duur * 60
        view = PollView(vraag, opts, timeout_secs, inter.user.id)

        embed = disnake.Embed(
            title="📊 Nieuwe Poll",
            description=vraag,
            color=disnake.Color.blurple(),
        ).set_footer(text=f"Gestart door {inter.user}", icon_url=inter.user.display_avatar.url)

        # Berichten sturen
        await inter.response.send_message(embed=embed, view=view)
        view.message = await inter.original_message()

        # Registreren
        active_polls[inter.guild.id] = view
        logger.info(
            "%s startte een poll in %s (%s)",
            inter.user,
            inter.guild.name,
            inter.guild.id,
        )


    @has_permissions(disnake.Permissions.administrator)
    @commands.slash_command(
        name="pollresults", description="Laat de huidige pollresultaten zien (privé)."
    )
    async def poll_results(self, inter: disnake.ApplicationCommandInteraction):
        view = active_polls.get(inter.guild.id)
        if not view:
            await inter.response.send_message(
                "Er is momenteel geen actieve poll.", ephemeral=True
            )
            return

        embed = disnake.Embed(
            title="📊 Huidige Pollresultaten",
            description=f"**{view.question}**\n\n{view.results_str()}",
            color=disnake.Color.orange(),
        )
        await inter.response.send_message(embed=embed, ephemeral=True)

    @has_permissions(disnake.Permissions.administrator)
    @commands.slash_command(name="pollvoters", description="Bekijk wie op wat heeft gestemd (alleen zichtbaar voor jou).")
    async def poll_voters(self, inter: disnake.ApplicationCommandInteraction):
        view = active_polls.get(inter.guild.id)
        if not view:
            await inter.response.send_message("Er is momenteel geen actieve poll.", ephemeral=True)
            return

        if not view.user_votes:
            await inter.response.send_message("Nog niemand heeft gestemd.", ephemeral=True)
            return

        # Maak overzicht
        voter_lines = []
        for user_id, option in view.user_votes.items():
            user = inter.guild.get_member(user_id)
            name = user.display_name if user else f"Onbekende gebruiker ({user_id})"
            voter_lines.append(f"**{name}** stemde op **{option}**")

        await inter.response.send_message("\n".join(voter_lines), ephemeral=True)



def setup(bot: commands.InteractionBot):
    bot.add_cog(Poll(bot))
