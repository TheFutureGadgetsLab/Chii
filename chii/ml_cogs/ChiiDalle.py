import numpy as np
import torch
from chii.body.CogSkeleton import CogSkeleton
from discord.ext import commands
from discord.ext.commands import Context
from min_dalle.TorchGen import DalleWrapper

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
            for _ in range(4):
                image = self.model(message)
                image = np.array(image)
            
                if image.max() != 0:
                    break
    
        self.model = self.model.to(self.cpu)
        torch.cuda.empty_cache()

        await ctx.send(
            file=self.image_file_from_array(
                img=image,
                fname="dalle",
                extension="png"
            )
        )

def setup(bot):
    bot.add_cog(ChiiDalle(bot))
