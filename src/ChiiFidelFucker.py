import random

from discord.ext import commands
from discord.ext.commands import Bot
from discord.message import Message

from src.CogSkeleton import CogSkeleton


class ChiiFidelFucker(CogSkeleton):
    FIDEL_ID = 207334663243563019

    def __init__(self, bot: Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id != self.FIDEL_ID:
            return

        if random.random() < 1.0/100.0:
            await self.alt_caps(message)
    
    async def alt_caps(self, message: Message):
        """ Change each character in message to alternating uppercase and lowercase """

        self.logger.info(f"Screwing with Fidel, alt caps: {message.content}")
        
        new_message = "".join([
            char.upper() if i % 2 == 0 else char.lower()
            for i, char in enumerate(message.content)
        ])
        await message.channel.send(new_message)

def setup(bot):
    bot.add_cog(ChiiFidelFucker(bot))