import io

import imageio.v3 as iio
import numpy as np
import onnxruntime as ort
import requests
import torch
import torchvision.transforms.functional as TF
from discord import Embed, File
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

from chii.body.CogSkeleton import CogSkeleton


class ChiiUpscale(CogSkeleton):
    """
    ChiiRepeat is a cog that will upscale the last image / gif sent
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.last_image = None
        self.last_message = None
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        self.ort_session = ort.InferenceSession(
            "data/sr_model.optimized.onnx",
            sess_options=sess_options,
            providers=['CUDAExecutionProvider']
        )

        self.register_hook(self.find_image)

    @commands.command(name='upscale')
    async def upscale(self, ctx: Context) -> None:
        if self.last_image is None or self.last_message is None:
            await ctx.send("Daddy I don't have an image to upscale :point_right: :point_left: send me one uwu")
            return

        try: 
            content = download_content(self.last_image)
        except:
            await ctx.send("Daddy wtf did you send me I can't download that :point_right: :point_left:")
            return

        await self.last_message.add_reaction("👍")

        out = []
        for frame in content:
            frame = np.expand_dims(frame, axis=0)
            sr = self.ort_session.run(None, {"input": frame})[0]
            out.append(sr)

        sr = np.squeeze(np.moveaxis(np.concatenate(out, axis=0), 1, -1))

        await self.send(sr, ctx)

    @commands.command(name='downscale')
    async def downscale(self, ctx: Context) -> None:
        if self.last_image is None or self.last_message is None:
            await ctx.send("Daddy I don't have an image to upscale :point_right: :point_left: send me one uwu")
            return

        try: 
            content = download_content(self.last_image)
        except:
            await ctx.send("Daddy wtf did you send me I can't download that :point_right: :point_left:")
            return

        await self.last_message.add_reaction("👍")

        out = []
        for frame in content:
            frame = np.expand_dims(frame, axis=0)
            frame = torch.from_numpy(frame)
            lr = TF.resize(frame, (frame.shape[2]//2, frame.shape[3]//2), TF.InterpolationMode.NEAREST)
            out.append(lr)

        lr = np.squeeze(np.moveaxis(np.concatenate(out, axis=0), 1, -1))

        await self.send(lr, ctx)

    async def send(self, sr: np.array, ctx: Context) -> None:
        if "mp4" in self.last_image:
            extension = ".mp4"
        else:
            extension = ".png"

        bytes_image = iio.imwrite("<bytes>", sr, extension=extension)
        byte_stream = io.BytesIO(bytes_image)
        await ctx.send(file=File(byte_stream, filename=f"upscaled{extension}"))

    async def find_image(self, msg: Message) -> None:
        found = False
        for embed in msg.embeds:
            if embed.image != Embed.Empty:
                self.last_image = embed.image.url
                self.last_message = msg
                found = True
            if embed.video != Embed.Empty:
                self.last_image = embed.video.url
                self.last_message = msg
                found = True
        
        for attach in msg.attachments:
            if attach.content_type.split("/")[0] in ["image", "video"]:
                self.last_image = attach.url
                self.last_message = msg
                found = True

        if found: 
            self.logger.info("Last image updated to: {}".format(self.last_image))

def download_content(url: str) -> np.array:
    res = requests.get(url, stream = True)
    content = iio.imread(res.content)

    if content.ndim == 3:
        content = content[None, ...]

    content = np.ascontiguousarray(
        np.moveaxis(content, -1, 1)
    )

    return content

def setup(bot):
    bot.add_cog(ChiiUpscale(bot))