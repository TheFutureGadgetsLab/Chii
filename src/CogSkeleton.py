import logging
from typing import List

from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context
from discord.message import Message
from random import random

LOG_FORMAT  ='%(levelname)s | %(asctime)s %(message)s'
DATE_FORMAT ='%m/%d/%Y %I:%M:%S %p'

class CogSkeleton(Cog):
    def __init__(self, bot: Bot):
        super().__init__()

        self.bot: Bot = bot

        self.logger = self.__setup_logger()

    @commands.Cog.listener()
    async def on_ready(self):
        """ Called when the client is done preparing the data received from Discord. Dont access API until this is called.
            This function is not guaranteed to only be called once. This library implements reconnection logic and thus
            will end up calling this event whenever a RESUME request fails.
        """
        pass

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """ Called when a message is received from Discord. """
        pass

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

    @property
    def __derived_name(self):
        return str(self.__class__.__name__)

    def __setup_logger(self, level=logging.INFO) -> logging.Logger:
        name     = self.__derived_name
        log_file = f'logs/{self.__derived_name}.log'

        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        logger.info(f'')
        logger.info(f'#'*80)
        logger.info(f'#')
        logger.info(f'# {name} Startup')
        logger.info(f'#')
        logger.info(f'#'*80)
        logger.info(f'')

        return logger

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        self.logger.error(str(error))
        print("-+"*40)
        print(self.__derived_name)
        print(error)