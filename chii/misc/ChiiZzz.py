import datetime as dt
from random import random, randrange
from time import time

from discord.ext import commands, tasks
from discord.message import Message

from chii.body.CogSkeleton import CogSkeleton


class ChiiZzz(CogSkeleton):
    """
    ChiiZzz send zzz when nobody has said anything for a while
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.last_message_time = time()
        self.chan = self.get_text_channel_by_name("general")
        self.time_threshold = 60 * 60 * 6

        self.register_hook(
            hook_func=self.update_last,
        )

    async def update_last(self, msg: Message) -> None:
        if msg.channel == self.chan:
            self.last_message_time = msg.created_at.timestamp()
    
    @tasks.loop(hours=5)
    async def send_zzz(self):
        if isNowInTimePeriod(dt.time(20,30), dt.time(9,30), dt.datetime.now().time()):
            return

        if (time() - self.last_message_time) > self.time_threshold and random() < 0.50:
            await self.chan.send("z" * randrange(3, 10) + "...")
            self.last_message_time = time()

#https://stackoverflow.com/a/39624147
def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 

def setup(bot):
    bot.add_cog(ChiiZzz(bot))
