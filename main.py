from discord.ext import commands
import discord

from src import load_token

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="The stupidest hyperintelligent discord bot you've ever seen.",
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.load_extension("src.ChiiWordleBot")
bot.load_extension("src.ChiiValGif")
bot.run(load_token())
