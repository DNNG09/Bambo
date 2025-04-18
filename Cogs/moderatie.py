import disnake
from disnake.ext import commands
from disnake.ext.commands import has_any_role
from dotenv import load_dotenv
import os
import datetime as dt
import helpers.logs

load_dotenv()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Moderation Cog is loaded")

    # KICK
    @commands.slash_command(description="Kick a user from the server as an admin")
    @has_any_role(os.getenv('admin_1'), os.getenv('admin_2'))
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        class KickConfirm(disnake.ui.View):
            @disnake.ui.button(label="✅ Bevestig kick", style=disnake.ButtonStyle.danger)
            async def confirm(self, button, interaction):
                if interaction.user != inter.user:
                    return await interaction.response.send_message("Niet jouw actie.", ephemeral=True)
                try:
                    await member.kick(reason=f"Kicked by {inter.user} – {reason}")
                    await interaction.response.edit_message(content=f"{member.mention} is gekickt.", view=None)
                except Exception as e:
                    await interaction.response.send_message(f"Kon {member} niet kicken. Fout: {e}", ephemeral=True)

            @disnake.ui.button(label="❌ Annuleer", style=disnake.ButtonStyle.secondary)
            async def cancel(self, button, interaction):
                if interaction.user == inter.user:
                    await interaction.response.edit_message(content="Kick geannuleerd.", view=None)

        await inter.response.send_message(f"Weet je zeker dat je {member.mention} wilt kicken?", view=KickConfirm(), ephemeral=True)

    # BAN
    @commands.slash_command(description="Ban een lid uit de server.")
    @has_any_role(os.getenv('admin_1'), os.getenv('admin_2'))
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        class BanConfirm(disnake.ui.View):
            @disnake.ui.button(label="✅ Bevestig ban", style=disnake.ButtonStyle.danger)
            async def confirm(self, button, interaction):
                if interaction.user != inter.user:
                    return await interaction.response.send_message("Niet jouw actie.", ephemeral=True)
                try:
                    await member.ban(reason=f"Banned by {inter.user} – {reason}")
                    await interaction.response.edit_message(content=f"{member.mention} is verbannen.", view=None)
                except Exception as e:
                    await interaction.response.send_message(f"Kon {member} niet bannen. Fout: {e}", ephemeral=True)

            @disnake.ui.button(label="❌ Cancel", style=disnake.ButtonStyle.secondary)
            async def cancel(self, button, interaction):
                if interaction.user == inter.user:
                    await interaction.response.edit_message(content="Ban geannuleerd.", view=None)

        await inter.response.send_message(f"Weet je zeker dat je {member.mention} wilt bannen?", view=BanConfirm(), ephemeral=True)

    # SOFTBAN
    @commands.slash_command(description="Softban (ban en unban om berichten te verwijderen).")
    @has_any_role(os.getenv('admin_1'), os.getenv('admin_2'))
    async def softban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        class SoftbanConfirm(disnake.ui.View):
            @disnake.ui.button(label="✅ Bevestig softban", style=disnake.ButtonStyle.danger)
            async def confirm(self, button, interaction):
                if interaction.user != inter.user:
                    return await interaction.response.send_message("Niet jouw actie.", ephemeral=True)
                try:
                    await member.ban(reason=f"Softbanned by {inter.user} – {reason}", delete_message_days=1)
                    await member.unban()
                    await interaction.response.edit_message(content=f"{member.name} is gesoftbanned.", view=None)
                except Exception as e:
                    await interaction.response.send_message(f"Softban mislukt. Fout: {e}", ephemeral=True)

            @disnake.ui.button(label="❌ Annuleer", style=disnake.ButtonStyle.secondary)
            async def cancel(self, button, interaction):
                if interaction.user == inter.user:
                    await interaction.response.edit_message(content="Softban geannuleerd.", view=None)

        await inter.response.send_message(f"Weet je zeker dat je {member.mention} wilt softbannen?", view=SoftbanConfirm(), ephemeral=True)




    # MUTE
    @commands.slash_command(description="Mute een lid tijdelijk via timeout.")
    @has_any_role(os.getenv('admin_1'), os.getenv('admin_2'))
    async def mute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, duration_minutes: int, reason: str):
        until = dt.datetime.now() + dt.timedelta(minutes=duration_minutes)
        try:
            await member.edit(timeout=until, reason=f"Muted by {inter.user} – {reason}")
            await inter.response.send_message(
                f"{member.mention} is gemute voor {duration_minutes} minuten.\nReden: {reason}",
                ephemeral=True
            )
        except Exception as e:
            await inter.response.send_message(f"❌ Mute mislukt.\nFout: {e}", ephemeral=True)
        
        if member.top_role >= inter.guild.me.top_role:
            return await inter.response.send_message(f"❌ Kan {member.mention} Don't mute: Their role is ", ephemeral=True)
    

        if member.guild_permissions.administrator:
            return await inter.response.send_message(
                f"❌ Kan {member.mention} Don't mute: They are an administrator.", ephemeral=True)






    # WARN
    @commands.slash_command(description="Geef een waarschuwing aan een lid.")
    @has_any_role(os.getenv('admin_1'), os.getenv('admin_2'))
    async def warn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        try:
            await member.send(f"⚠️ {member}, je bent gewaarschuwd in **{inter.guild.name}**:\n{reason}")
            await inter.response.send_message(f"{member.mention} is gewaarschuwd.", ephemeral=True)
        except Exception:
            await inter.response.send_message(f"⚠️ Kon {member.mention} niet waarschuwen via DM, maar waarschuwing is wel uitgegeven.", ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
