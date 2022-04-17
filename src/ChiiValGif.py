from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context
from discord.message import Message
from src.CogSkeleton import CogSkeleton
import random

class ChiiValGif(CogSkeleton):
    GIF_LINKS = [
        'https://tenor.com/view/valorant-play-valorant-hop-on-valorant-hop-on-anime-kissing-gif-23656387',
        'https://c.tenor.com/rhNlcxoiD_QAAAAC/valorant.gif',
        'https://tenor.com/view/iahtethis-gif-21851946'
    ]
    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """ When a user mentions 'valorant' or 'val', choose a random link from GIF_LINKS and send it """
        if message.author.id == self.bot.user.id:
            return

        if 'valorant' in message.content.lower() or 'val' in message.content.lower():
            self.logger.info(f"Sent gif, triggered by '{message.content}'")
            await self.send_message(message)

    async def send_message(self, message: Message):
        await message.channel.send(random.choice(self.GIF_LINKS))


def setup(bot):
    bot.add_cog(ChiiValGif(bot))