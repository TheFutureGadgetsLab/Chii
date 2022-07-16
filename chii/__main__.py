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

bot.load_extension("chii.misc.ChiiWordleCog")
bot.load_extension("chii.misc.ChiiValCog")
bot.load_extension("chii.misc.ChiiFidelFucker")
bot.load_extension("chii.misc.ChiiPresenceCog")
bot.load_extension("chii.misc.ChiiRepeat")
bot.load_extension("chii.misc.ChiiBlahBlah")
bot.load_extension("chii.misc.ChiiScream")
bot.load_extension("chii.misc.ChiiShh")
bot.load_extension("chii.misc.ChiiZzz")
bot.load_extension("chii.misc.ChiiTFTCog")
bot.load_extension("chii.misc.ChiiFarmCog")

# ML Cogs
bot.load_extension("chii.ml_cogs.ChiiUpscale")
bot.load_extension("chii.ml_cogs.ChiiDalle")

with open("token.txt", "r") as token_file:
    token = token_file.read().strip()
bot.run(token)
