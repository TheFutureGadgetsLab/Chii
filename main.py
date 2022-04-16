from src import load_token
from discord.ext import commands

import logging
logging.basicConfig(
    filename='chii.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(levelname)s | %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="The stupidest hyperintelligent discord bot you've ever seen."
)

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}")

bot.load_extension("src.ChiiWordleBot")
bot.run(load_token())