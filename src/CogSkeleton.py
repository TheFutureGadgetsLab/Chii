import logging

from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context
from discord.message import Message

LOG_FORMAT  ='%(levelname)s | %(asctime)s %(message)s'
DATE_FORMAT ='%m/%d/%Y %I:%M:%S %p'

class CogSkeleton(Cog):
    def __init__(self, bot: Bot):
        super().__init__()

        self.bot: Bot = bot

        self.logger = self.__setup_logger(self.__derived_name, f'logs/{self.__derived_name}.log')

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

    @property
    def __derived_name(self):
        return str(self.__class__.__name__)

    def __setup_logger(self, name, log_file, level=logging.INFO) -> logging.Logger:
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger
