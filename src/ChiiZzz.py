from random import random, randrange
from time import time

from discord.ext import commands, tasks
from discord.message import Message

from src.CogSkeleton import CogSkeleton

class ChiiZzz(CogSkeleton):
    """
    ChiiZzz send zzz when nobody has said anything for a while
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.last_message_time = time()
        self.chan = self.get_text_channel_by_name("general")
        self.time_threshold = 60 * 60 * 6

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
        if msg.channel == self.chan:
            self.last_message_time = msg.created_at.timestamp()
    
    @tasks.loop(hours=5)
    async def send_zzz(self):
        if (time() - self.last_message_time) > self.time_threshold and random() < 0.50:
            await self.chan.send("z" * randrange(3, 10) + "...")
            self.last_message_time = time()

def setup(bot):
    bot.add_cog(ChiiZzz(bot))
