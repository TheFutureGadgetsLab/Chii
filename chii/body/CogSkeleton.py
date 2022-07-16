from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context
from chii.body.DiscordLimb import DiscordLimb
from chii.body.HookLimb import HookLimb
from chii.body.LoggerLimb import LoggerLimb
from chii.body.MiscLimb import MiscLimb


class CogSkeleton(DiscordLimb, LoggerLimb, MiscLimb, HookLimb, Cog):
    def __init__(self, bot: Bot):
        super(Cog, self).__init__()

        self.bot: Bot = bot
        self.logger = self._setup_logger()
    
        self.hooks = []

    @commands.Cog.listener()
    async def on_message(self, message: Context) -> None:
        await self.process_hooks(message)
