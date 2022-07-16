from random import randrange

from discord.ext import commands
from discord.message import Message

from chii.body.CogSkeleton import CogSkeleton


class ChiiScream(CogSkeleton):
    """
    ChiiScream is a cog that screams whenever someone uses all-caps
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

        self.register_hook(
            hook_func=self.scream,
            ignore_bot=True,
            with_prob=0.4
        )

    async def scream(self, msg: Message) -> None:
        uppercase_count = 0
        total_count = 0
        for char in msg.content:
            if char.isalpha():
                if char.isupper():
                    uppercase_count += 1
                total_count += 1

        if total_count > 3 and uppercase_count / total_count > 0.85:
            await msg.channel.send("A" * randrange(3, 40) + "!" * randrange(1, 8))

def setup(bot):
    bot.add_cog(ChiiScream(bot))
