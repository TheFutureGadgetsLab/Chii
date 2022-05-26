from random import random
from typing import List

from discord.channel import TextChannel


class MiscLimb:
    def get_text_channels(self, ignore_bot_testing=True) -> List[TextChannel]:
        """ Returns a list of all text channels """
        channels = [channel for channel in self.bot.get_all_channels() if isinstance(channel, TextChannel)]

        if ignore_bot_testing:
            channels = [channel for channel in channels if channel.name != "bot-testing"]

        return channels
    
    def get_text_channel_by_name(self, name: str) -> TextChannel:
        """ Returns a text channel by name """
        channels = self.get_text_channels()

        for channel in channels:
            if channel.name == name:
                return channel

        return None

    async def send_with_prob(self, channel: TextChannel, message: str, prob: float) -> None:
        if random() < prob:
            await channel.send(message)
