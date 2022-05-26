from discord.ext import commands
from discord.message import Message

class DiscordLimb:
    """ Effectively contains documentation for the useful pycord functions. """

    @commands.Cog.listener()
    async def on_ready(self)-> None:
        """ Called when the client is done preparing the data received from Discord. Dont access API until this is called.
            This function is not guaranteed to only be called once. This library implements reconnection logic and thus
            will end up calling this event whenever a RESUME request fails.
        """
        pass

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """ Called when a message is received from Discord. """
        pass