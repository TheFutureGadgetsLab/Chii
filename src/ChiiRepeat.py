from random import random

from discord.ext import commands
from discord.message import Message

from src.CogSkeleton import CogSkeleton

class ChiiRepeat(CogSkeleton):
    """
    ChiiRepeat is a cog that copy-cats whenever multiple people say the same thing
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.last_repeated_msg = None
        self.repeated_count = 0

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
        m: str = msg.content.lower().strip()

        if self.last_repeated_msg == m:
            # Message was repeated
            self.repeated_count += 1
            if self.repeated_count >= 2:
                await msg.channel.send(f"{self.last_repeated_msg}")
        else:
            # Reset
            self.repeated_count = 0
        self.last_repeated_msg = m

def setup(bot):
    bot.add_cog(ChiiRepeat(bot))