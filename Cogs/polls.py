import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import has_any_role
from disnake.ui import View, Button, Select
import datetime as dt
import logging

logger = logging.getLogger("polls")

active_polls = {}  # {guild_id: PollView}


class PollView(View):
    def __init__(self, question, options, timeout, author_id):
        super().__init__(timeout=timeout)
        self.question = question
        self.options = options
        self.votes = {opt: 0 for opt in options}
        self.user_votes = {}
        self.author_id = author_id
        self.message = None
        self.closed = False

        if len(options) <= 5:
            for i, opt in enumerate(options):
                emoji = chr(127462 + i)  # 🇦 - 🇪
                self.add_item(PollButton(label=opt, custom_id=opt, emoji=emoji))
        else:
            self.add_item(PollDropdown(options))

    def vote(self, user_id, option):
        if user_id in self.user_votes:
            prev = self.user_votes[user_id]
            if prev == option:
                return False
            self.votes[prev] -= 1

        self.user_votes[user_id] = option
        self.votes[option] += 1
        return True

    def get_results(self):
        total = sum(self.votes.values()) or 1
        return "\n".join(
            f"**{opt}** — {v} vote(s) ({round((v/total)*100)}%)" for opt, v in self.votes.items()
        )

    async def on_timeout(self):
        await self.close_poll()

    async def close_poll(self):
        if self.closed:
            return
        self.closed = True
        for child in self.children:
            child.disabled = True

        result_embed = disnake.Embed(
            title="📊 Poll Results",
            description=f"**{self.question}**\n\n{self.get_results()}",
            color=disnake.Color.green(),
        )
        await self.message.edit(embed=result_embed, view=self)
        active_polls.pop(self.message.guild.id, None)



class PollButton(Button):
    def __init__(self, label, custom_id, emoji):
        super().__init__(label=label, custom_id=custom_id, style=disnake.ButtonStyle.blurple, emoji=emoji)

    async def callback(self, interaction: disnake.MessageInteraction):
        view: PollView = self.view
        if view.vote(interaction.user.id, self.custom_id):
            await interaction.response.send_message(f"You voted for **{self.custom_id}**", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already voted for **{self.custom_id}**!", ephemeral=True)


class PollDropdown(Select):
    def __init__(self, options):
        opts = [disnake.SelectOption(label=o, value=o) for o in options]
        super().__init__(placeholder="Choose an option", min_values=1, max_values=1, options=opts)

    async def callback(self, interaction: disnake.MessageInteraction):
        view: PollView = self.view
        option = interaction.data["values"][0]
        if view.vote(interaction.user.id, option):
            await interaction.response.send_message(f"You voted for **{option}**", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already voted for **{option}**!", ephemeral=True)


class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Poll Cog is loaded")



    @commands.slash_command(description="Create a poll with up to 25 options.")
    async def poll(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question: str,
        duration: int = commands.Param(gt=0, le=60, description="Duration in minutes (max 60)"),
        option1: str = commands.Param(),
        option2: str = commands.Param(),
        option3: str = None,
        option4: str = None,
        option5: str = None,
        option6: str = None,
        option7: str = None,
        option8: str = None,
        option9: str = None,
        option10: str = None,
    ):
        options = [opt for opt in [option1, option2, option3, option4, option5,
                                   option6, option7, option8, option9, option10] if opt]

        if len(options) < 2:
            await inter.send("Je moet minstens 2 opties opgeven.", ephemeral=True)
            return

        view = PollView(question, options, timeout=duration * 60, author_id=inter.user.id)
        embed = disnake.Embed(title="📊 New Poll", description=question, color=disnake.Color.blurple())
        embed.set_footer(text=f"Poll by {inter.user.name}", icon_url=inter.user.display_avatar.url)

        await inter.response.send_message(embed=embed, view=view)
        message = await inter.original_message()
        view.message = message
        active_polls[inter.guild.id] = view


    @commands.slash_command(description="Toon de resultaten van de laatste poll.")
    async def pollresults(self, inter: disnake.ApplicationCommandInteraction):
        view = active_polls.get(inter.guild.id)
        if not view:
            await inter.send("Er is geen actieve poll in deze server.", ephemeral=True)
            return

        embed = disnake.Embed(
            title="📊 Huidige Pollresultaten",
            description=f"**{view.question}**\n\n{view.get_results()}",
            color=disnake.Color.orange(),
        )
        await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(poll(bot))
