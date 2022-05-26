from random import choice, randrange

from discord.ext import commands
from discord.message import Message

from src.body.CogSkeleton import CogSkeleton

class ChiiShh(CogSkeleton):
    """
    ChiiShh is a cog that shh's randomly
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.register_hook(
            hook_func=self.shh,
            ignore_bot=True,
            with_prob=0.01,
        )

    async def shh(self, msg: Message) -> None:
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
            "have a lot to say today don't we",
        ]
        await msg.channel.send(choice(msgs))

def setup(bot):
    bot.add_cog(ChiiShh(bot))
