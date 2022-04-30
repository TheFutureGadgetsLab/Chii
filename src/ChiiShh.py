from random import randrange, random

from discord.ext import commands
from discord.message import Message

from src.CogSkeleton import CogSkeleton

class ChiiShh(CogSkeleton):
    """
    ChiiShh is a cog that shh's randomly
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
        if random() < 0.01:
            msgs = [
                "s" + "h" * randrange(2, 10),
                "no",
                f"shut {'u' * randrange(1,8)}p",
                f"shut the fuck {'u' * randrange(1,8)}p",
                "stfu",
                f"st{'o' * randrange(1,8)}p",
                "stop talking please",
                "please stop talking",
                "loud today aren't we",
                "have a lot to say today dont't we",
            ]
            await msg.channel.send(msgs[randrange(0, len(msgs))])

def setup(bot):
    bot.add_cog(ChiiShh(bot))
