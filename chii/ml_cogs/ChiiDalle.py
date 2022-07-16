import io

import imageio.v3 as iio
import numpy as np
import torch
from discord import File
from discord.ext import commands
from discord.ext.commands import Context
from min_dalle.TorchGen import DalleWrapper

from chii.body.CogSkeleton import CogSkeleton

torch.set_grad_enabled(False)
torch.backends.cudnn.benchmark = True

class ChiiDalle(CogSkeleton):
    """
    ChiiRepeat is a cog that will upscale the last image / gif sent
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.model = DalleWrapper(is_mega=False)
        self.model.freeze()

        self.device = torch.device("cuda")
        self.cpu    = torch.device("cpu")

    @commands.command(name='dalle')
    async def dalle(self, ctx: Context, *args) -> None:
        message = " ".join(args)

        self.model = self.model.to(self.device)
        with torch.inference_mode(), torch.cuda.amp.autocast():
            image = self.model(message)
        self.model = self.model.to(self.cpu)
        torch.cuda.empty_cache()

        image = np.array(image)

        bytes_image = iio.imwrite("<bytes>", image, extension=".png")
        byte_stream = io.BytesIO(bytes_image)
        await ctx.send(file=File(byte_stream, filename=f"dalle.png"))

def setup(bot):
    bot.add_cog(ChiiDalle(bot))
