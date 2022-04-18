from discord.ext import commands
import discord

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="The stupidest hyperintelligent discord bot you've ever seen.",
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.load_extension("src.ChiiWordleCog")
bot.load_extension("src.ChiiValCog")
bot.load_extension("src.ChiiPresenceCog")

with open("token.txt", "r") as token_file:
    token = token_file.read().strip()
bot.run(token)
