import random
import re

from discord.ext.commands import Bot
from discord.message import Message

from src.body.CogSkeleton import CogSkeleton


class ChiiTFTCog(CogSkeleton):
    GIF_LINKS = [
        'https://c.tenor.com/dw6MV3mJADsAAAAC/hop-on-tft.gif',
        'https://c.tenor.com/-0XzArRAmAYAAAAd/powder-jinx.gif',
        'https://c.tenor.com/d7E5fR7m87oAAAAC/mewhennotft-no.gif',
        'https://c.tenor.com/copo9zmux4wAAAAd/tft-team-fight-tactics.gif',
        'https://c.tenor.com/A_p2FQmsUaIAAAAC/wanna-play-tft-tft.gif',
        'https://c.tenor.com/A_p2FQmsUaIAAAAC/wanna-play-tft-tft.gif',
        'https://c.tenor.com/fh53G98IVPsAAAAd/hop-on-tft.gif',
        'https://c.tenor.com/d3TXEhDRkeIAAAAd/hopontft-tft.gif',
        'https://c.tenor.com/JOBMzQIE_ZgAAAAC/tft-taine.gif',
        'https://c.tenor.com/ppP7LRnzHIEAAAAC/tft.gif',
        'https://c.tenor.com/IsaW3XFddp8AAAAd/tft-teamfight-tactics.gif',
        'https://c.tenor.com/yNrDz1h5rJcAAAAd/hopontft-hop.gif',
        'https://c.tenor.com/3mqYPdMFH6cAAAAd/nana-stop.gif',
        'https://c.tenor.com/plJDstejhf8AAAAd/cat-whip.gif',
        'https://c.tenor.com/copo9zmux4wAAAAd/tft-team-fight-tactics.gif'
    ]

    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.register_hook(
            hook_func=self.on_tft,
            condition=lambda message: re.search(r"(\btft\b)|(team fight tactics)", message.content, re.IGNORECASE),
            ignore_bot=True,
            with_prob=1.0,
        )

    async def on_tft(self, message: Message) -> None:
        """ When a user mentions 'team fight tactics' or 'tft', choose a random link from GIF_LINKS and send it """
        self.logger.info(f"Sent gif, triggered by '{message.content}'")
        await message.channel.send(random.choice(self.GIF_LINKS))

def setup(bot):
    bot.add_cog(ChiiTFTCog(bot))
