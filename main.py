import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv
from database import Database
import logging
import helpers.logs
import os

load_dotenv()

bot = commands.Bot(intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    await bot.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.playing,
            name="Hi daar! Als ik wat voor je kan doen, vergeet dan zeker niet om een ticket in te dienen!"
        )
    )

@tasks.loop(minutes=1)
async def keep_database_active():
    print("Keeping the database active...")

    try:
        Database.cursor.execute("SELECT * FROM leveling")
        Database.cursor.fetchall()
    except Exception as error:
        print(f"Something went in main.py: {error}")
        logging.warning("Database went down, please check the status!")

keep_database_active.start()
bot.load_extension('Cogs.serverlogging')
bot.load_extension('Cogs.welcome')
bot.load_extension('Cogs.counting')
bot.load_extension('Cogs.qotd')
bot.load_extension('Cogs.messages')
bot.load_extension('Cogs.polls')
bot.load_extension('Cogs.help')
bot.load_extension('Cogs.games')
bot.load_extension('Cogs.tools')


bot.run(os.getenv('TOKEN'))