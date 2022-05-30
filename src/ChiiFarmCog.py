from fileinput import filename
from src.body.CogSkeleton import CogSkeleton
from discord import FFmpegPCMAudio, ClientException
from discord.ext import commands
from discord.ext.commands import Context
import time
class ChiiFarmCog(CogSkeleton):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.command(name='pig')
    async def pig(self, ctx: Context):
        await play_audio(ctx, "./data/Pig.mp3")
        time.sleep(5)
        await ctx.send("Oink Oink Oink")
        await ctx.voice_client.disconnect()

    @commands.command(name='goat')
    async def goat(self, ctx: Context):
        await play_audio(ctx, "./data/Goat.mp3")
        time.sleep(5)
        await ctx.send("Ahhhhh")
        await ctx.voice_client.disconnect()

async def play_audio(ctx, fileName):
    channel = ctx.author.voice.channel
    try:
        await channel.connect()
    except AttributeError:
        await ctx.send("You're not in a voice_channel mistah")
    except ClientException:
        #occurs if Chii is already connected
        pass
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.play(FFmpegPCMAudio(executable="ffmpeg", source=fileName))
    

def setup(bot):
    bot.add_cog(ChiiFarmCog(bot))
