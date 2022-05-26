from discord.ext.commands import Bot
from discord.message import Message

from src.body.CogSkeleton import CogSkeleton


class ChiiFidelFucker(CogSkeleton):
    FIDEL_ID = 207334663243563019

    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.register_hook(
            hook_func=self.alt_cap,
            condition=lambda message: message.author.id == self.FIDEL_ID,
            ignore_bot=True,
            with_prob=1.0/100.0,
        )

    async def alt_cap(self, message: Message):
        self.logger.info(f"Screwing with Fidel, alt caps: {message.content}")
        
        new_message = "".join([
            char.upper() if i % 2 == 0 else char.lower()
            for i, char in enumerate(message.content)
        ])
        await message.channel.send(new_message)

def setup(bot):
    bot.add_cog(ChiiFidelFucker(bot))
