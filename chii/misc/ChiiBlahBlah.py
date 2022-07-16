from random import random

from discord.ext import tasks, commands
from discord.message import Message

from chii.body.CogSkeleton import CogSkeleton

class ChiiBlahBlah(CogSkeleton):
    """
    ChiiBlahBlah is a cog that says blah blah blah when message send rate is high
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.msg_count = 0
        self.threshold = 2.5 # messages per second to trigger
        self.cooldown = 15.0 # seconds to wait before triggering again
        self.to_channel = None # channel to send to

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
        self.msg_count += 1
        self.to_channel = msg.channel
    
    @tasks.loop(seconds=3)
    async def change_presence(self):
        if not self.is_ready or self.to_channel is None:
            return
        msgs_per_sec = self.msg_count / 3.0
        self.msg_count = 0
        if msgs_per_sec > self.threshold:
            await self.to_channel.send("blah " * random.randrange(1, 7))

def setup(bot):
    bot.add_cog(ChiiBlahBlah(bot))
