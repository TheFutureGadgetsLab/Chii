from discord.ext import commands
import discord
from tabulate import tabulate

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="The stupidest hyperintelligent discord bot you've ever seen.",
    intents=discord.Intents.all()
)

@bot.command()
@commands.is_owner()
async def reload(ctx):
    extensions = list(bot.extensions.keys())
    table = []
    for extension in extensions:
        pname = extension.split(".")[-1]
        try:
            bot.reload_extension(extension)
            status = "✅"
        except:
            status = "⛔"
        table.append((pname, status))

    toprint = f"```\n{tabulate(table, headers=['Cog', 'Status'])}\n```"
    embed = discord.Embed(title='Reloaded', description=toprint, color=0xff00c8)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.load_extension("src.ChiiWordleCog")
bot.load_extension("src.ChiiValCog")
bot.load_extension("src.ChiiFidelFucker")
bot.load_extension("src.ChiiPresenceCog")
bot.load_extension("src.ChiiRepeat")
bot.load_extension("src.ChiiBlahBlah")
bot.load_extension("src.ChiiScream")
bot.load_extension("src.ChiiUpscale")
bot.load_extension("src.ChiiShh")
bot.load_extension("src.ChiiZzz")
bot.load_extension("src.ChiiTFTCog")
bot.load_extension("src.ChiiFarmCog")

with open("token.txt", "r") as token_file:
    token = token_file.read().strip()
bot.run(token)
