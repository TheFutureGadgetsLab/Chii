from random import randrange

from discord.ext import commands
from discord.message import Message

from src.CogSkeleton import CogSkeleton

class ChiiScream(CogSkeleton):
    """
    ChiiScream is a cog that screams whenever someone uses all-caps
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message(self, msg: Message) -> None:
        if msg.author.id == self.bot.user.id:
            return
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
