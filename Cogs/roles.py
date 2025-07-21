import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Roles Cog is loaded")


    @commands.slash_command(name="role_add", description="Add a role to yourself")
    async def role_add(self, inter: disnake.AppCmdInter, role: disnake.Role):
        if role.permissions.administrator:
            await inter.send("You cannot add an administrator role to yourself.", ephemeral=True)
            return
        else:
            await inter.author.add_roles(role)
            await inter.send(f"Role {role.name} has been added to you.")

    @commands.slash_command(name="role_remove", description="Remove a role from yourself")
    async def role_remove(self, inter: disnake.AppCmdInter, role: disnake.Role):
        if role.permissions.administrator:
            await inter.send("You cannot remove an administrator role from yourself.\n Ask the Server Owner for assistance.", ephemeral=True)
            return
        else:
            await inter.author.remove_roles(role)
            await inter.send(f"Role {role.name} has been removed from you.", ephemeral=True)
    
    @commands.slash_command(name="role_list", description="List all available roles")
    async def role_list(self, inter: disnake.AppCmdInter):
        roles = [role.name for role in inter.guild.roles if not role.is_default() and not role.managed]
        await inter.send("Available roles:\n" + "\n".join(roles), ephemeral=True)

    @commands.slash_command(name="role_info", description="Get information about a role")
    async def role_info(self, inter: disnake.AppCmdInter, role: disnake.Role):
        embed = disnake.Embed(title=f"Role Information: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name="Members", value=len(role.members))
        await inter.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Roles(bot))