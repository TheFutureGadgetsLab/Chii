import imageio.v3 as iio
import numpy as np
import onnxruntime as ort
import requests
import torch
import torchvision.transforms.functional as TF
from chii.body.CogSkeleton import CogSkeleton
from chii.Emojis import Emoji
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message
from PIL import Image


class ChiiUpscale(CogSkeleton):
    """
    ChiiRepeat is a cog that will upscale the last image / gif sent
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.last_image: str       = None
        self.last_message: Message = None

        self.register_hook(self.register_image)

    @commands.command(name='upscale')
    async def upscale(self, ctx: Context) -> None:
        if self.last_image is None or self.last_message is None:
            await ctx.send(f"Daddy I don't have an image to upscale {Emoji.point_rl} send me one uwu")
            return

        try:
            content = download_content(self.last_image)
        except:
            await ctx.send(f"Daddy wtf did you send me I can't download that {Emoji.point_rl}")
            return

        await self.last_message.add_reaction(Emoji.thumbs_up)

        sess = self.build_session()
        out = []
        for frame in content:
            frame = np.expand_dims(frame, axis=0)
            sr = sess.run(None, {"input": frame})[0]
            out.append(sr)

        sr = np.squeeze(np.moveaxis(np.concatenate(out, axis=0), 1, -1))

        await ctx.send(
            file=self.image_file_from_array(
                img=sr,
                fname="upscaled",
                extension="png" if "png" in self.last_image else "mp4"
            )
        )

    @commands.command(name='downscale')
    async def downscale(self, ctx: Context) -> None:
        if self.last_image is None or self.last_message is None:
            await ctx.send(f"Daddy I don't have an image to upscale {Emoji.point_rl} send me one uwu")
            return

        try:
            content = download_content(self.last_image)
        except:
            await ctx.send(f"Daddy wtf did you send me I can't download that {Emoji.point_rl}")
            return

        await self.last_message.add_reaction(Emoji.thumbs_up)

        out = []
        for frame in content:
            frame = np.expand_dims(frame, axis=0)
            frame = torch.from_numpy(frame)
            lr = TF.resize(frame, (frame.shape[2]//2, frame.shape[3]//2), TF.InterpolationMode.NEAREST)
            out.append(lr)

        lr = np.squeeze(np.moveaxis(np.concatenate(out, axis=0), 1, -1))

        await ctx.send(
            file=self.image_file_from_array(
                img=lr,
                fname="downscaled",
                extension="png" if "png" in self.last_image else "mp4"
            )
        )

    async def register_image(self, msg: Message) -> None:
        if (img_url := self.find_image_in_message(msg)) is None:
            return

        self.last_image   = img_url
        self.last_message = msg

        self.logger.info("Last image updated to: {}".format(self.last_image))

    def build_session(self) -> ort.InferenceSession:
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        return ort.InferenceSession(
            "data/sr_model.optimized.onnx",
            sess_options=sess_options,
            providers=['CUDAExecutionProvider']
        )

def download_content(url: str) -> np.array:
    res = requests.get(url, stream = True)
    content = iio.imread(res.content)

    # Convert to RGB
    content = np.array(Image.fromarray(content).convert('RGB'))

    if content.ndim == 3:
        content = content[None, ...]

    content = np.ascontiguousarray(
        np.moveaxis(content, -1, 1)
    )

    return content

def setup(bot):
    bot.add_cog(ChiiUpscale(bot))
