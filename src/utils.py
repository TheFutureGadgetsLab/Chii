from typing import List
from discord.ext import commands
from discord.channel import TextChannel

def get_text_channels(bot: commands.Bot, ignore_bot_testing=True) -> List[TextChannel]:
    """ Returns a list of all text channels """
    channels = [channel for channel in bot.get_all_channels() if isinstance(channel, TextChannel)]

    if ignore_bot_testing:
        channels = [channel for channel in channels if channel.name != "bot-testing"]

    return channels

def load_token() -> str:
    """ Loads the bot token from disk """
    with open("token.txt", "r") as token_file:
        token = token_file.read().strip()
    return token