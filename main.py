from discord.ext import commands

from src import load_token

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="The stupidest hyperintelligent discord bot you've ever seen."
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.load_extension("src.ChiiWordleBot")
bot.run(load_token())
