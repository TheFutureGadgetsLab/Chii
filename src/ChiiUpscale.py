import mimetypes
import os
import shutil
import tempfile

import requests
import torch
import torchvision as tv
from discord import Embed, File
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

from src.body.CogSkeleton import CogSkeleton
import onnxruntime as ort

torch.set_grad_enabled(False)

class ChiiUpscale(CogSkeleton):
    """
    ChiiRepeat is a cog that will upscale the last image / gif sent
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.last_image = None

        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.ort_session = ort.InferenceSession(
            "data/sr_model.optimized.onnx",
            sess_options=sess_options,
            providers=['CPUExecutionProvider']
        )

    @commands.command(name='upscale')
    async def upscale(self, ctx: Context) -> None:
        if self.last_image is None:
            await ctx.send("Daddy I don't have an image to upscale :(")
            return
        
        res = requests.get(self.last_image, stream = True)

        if res.status_code != 200:
            await ctx.send("Daddy I can't upscale that image :(")
            return

        infile = tempfile.NamedTemporaryFile()
        shutil.copyfileobj(res.raw, infile)

        fmt, _ = mimetypes.guess_type(self.last_image)
        if 'image' in fmt:
            inp = [tv.io.read_image(infile.name, mode=tv.io.ImageReadMode.RGB),]
        elif 'video' in fmt:
            inp, audio, meta  = tv.io.read_video(infile.name)
            inp = inp.movedim(-1, 1).contiguous()
        else:
            await ctx.send("Daddy I got something stuck in my buffer and idk what it is :(")
            return

        out = []
        for img in inp:
            sr = self.ort_session.run(None, {"input": img.numpy()})[0]
            sr = torch.from_numpy(sr)
            out.append(sr)

        sr = torch.stack(out).squeeze()

        if 'image' in fmt:
            outfile = tempfile.NamedTemporaryFile()
            tv.io.write_png(sr, outfile.name)
            await ctx.send(file=File(outfile.name, filename=f"upscaled.{fmt.split('/')[1]}"))
            outfile.close()
        elif 'video' in fmt:
            outfile = f"{tempfile.gettempdir()}/upscaled.mp4"
            tv.io.write_video(outfile, sr.movedim(1, -1), fps=meta['video_fps'])
            await ctx.send(file=File(outfile, filename=f"upscaled.mp4"))
            os.remove(outfile)


    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
        self.update_img(msg)

    def update_img(self, msg: Message):
        """ 
            Check if the message contains an image / gif and update last image
        """
        self.detect_attachment(msg)
        self.detect_embed(msg)

        self.logger.info("Last image updated to: {}".format(self.last_image))

    def detect_attachment(self, msg: Message):
        if len(msg.attachments) == 0:
            return

        self.last_image = msg.attachments[0].url

    def detect_embed(self, msg: Message):
        if len(msg.embeds) == 0:
            return
        
        embed = msg.embeds[0]
        if embed.image.url != Embed.Empty:
            self.last_image = embed.image.url
        elif embed.video.url != Embed.Empty:
            self.last_image = embed.video.url

def setup(bot):
    bot.add_cog(ChiiUpscale(bot))
