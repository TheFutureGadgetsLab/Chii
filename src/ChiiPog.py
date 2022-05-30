from email.mime import audio
from src.body.CogSkeleton import CogSkeleton
from discord import Embed, File, FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

class ChiiPog(CogSkeleton):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.command(name='join_vc')
    async def join(self, ctx: Context):
        channel = ctx.author.voice.channel
        await channel.connect()
        await channel.play(FFmpegPCMAudio(executable="ffmpeg.exe", source="Pig.mp3"))
        await ctx.send("Oink Oink Oink")

    @commands.command(name='go_away')
    async def leave(self, ctx: Context):
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(ChiiPog(bot))
