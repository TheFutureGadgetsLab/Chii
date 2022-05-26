import random
import re

from discord.ext.commands import Bot
from discord.message import Message

from src.body.CogSkeleton import CogSkeleton


class ChiiValCog(CogSkeleton):
    GIF_LINKS = [
        'https://c.tenor.com/AmoBE7GHZpkAAAAC/valorant-play-valorant.gif',
        'https://c.tenor.com/rhNlcxoiD_QAAAAC/valorant.gif',
        'https://c.tenor.com/xaKjzheIdEUAAAAC/iahtethis.gif',
        'https://c.tenor.com/yHC9Hw8aMBMAAAAC/hop-on-val-valorant.gif',
        'https://c.tenor.com/RyaD6p3F6ZIAAAAC/valorant-get-on-valorant.gif',
        'https://c.tenor.com/wq06F7HScjQAAAAC/valorant-pbe.gif',
        'https://c.tenor.com/BleThQtSxFsAAAAC/death-note-l-lawliet.gif',
        'https://c.tenor.com/e7bjIqmpHScAAAAC/hiko-100thieves.gif',
    ]

    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.register_hook(
            hook_func=self.on_val,
            condition=lambda message: re.search(r"(\bval\b)|(valorant)", message.content, re.IGNORECASE),
            ignore_bot=True,
            with_prob=1.0,
        )

    async def on_val(self, message: Message) -> None:
        """ When a user mentions 'valorant' or 'val', choose a random link from GIF_LINKS and send it """
        self.logger.info(f"Sent gif, triggered by '{message.content}'")
        await message.channel.send(random.choice(self.GIF_LINKS))

def setup(bot):
    bot.add_cog(ChiiValCog(bot))
