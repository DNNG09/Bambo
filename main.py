import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
import logging
import helpers.logs

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
logging.info("Database still active")

bot.load_extension('Cogs.serverlogging')
logging.info("Serverlogging Loaded")
bot.load_extension('Cogs.moderatie')
logging.info("Moderation Cog Loaded")
bot.load_extension('Cogs.anti_bot')
logging.info("Serverlogging Loaded")
bot.load_extension('Cogs.messages')
logging.info("Messages Loaded")
bot.load_extension('Cogs.counting')
logging.info("Counting Loaded")
bot.load_extension('Cogs.bump')
logging.info("Bump Loaded")
bot.load_extension('Cogs.polls')
logging.info("Pollmaker Loaded")


bot.run(Secrets.TOKEN)