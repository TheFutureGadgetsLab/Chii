import os
import re
from collections import namedtuple
from typing import Optional

import pandas as pd
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

from src import utils
import logging

WordleResult = namedtuple('WordleResult', ['day', 'tries', 'user'])

DF_PATH = "data/wordle.csv"

class ChiiWordleBot(commands.Cog):
    """
    ChiiWordleBot is a cog that scans messages for wordle results and
    creates a leaderboard based on user performance
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot

        # Stores results
        self.dataframe: pd.DataFrame = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_dataframe()

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        entry = self.update_dataframe(message)

        if entry is not None:
            await message.channel.send(f"Thanks for your submission, {entry.user}, you suck ass :)")

    @commands.command(name='wordle_leaderboard')
    async def leaderboard(self, ctx: Context) -> None:
        string = format_leaderboard(self.dataframe)
        string = f"```\n{string}```"
        await ctx.send(string)

    async def load_dataframe(self) -> None:
        """ Loads the dataframe from the csv file """

        if os.path.exists(DF_PATH):
            self.dataframe = pd.read_csv(DF_PATH)
        else:
            self.dataframe = pd.DataFrame(columns=["day", "tries", "user"])
            await self.initial_populate()

    def update_dataframe(self, message: Message) -> Optional[WordleResult]:
        """ Updates the dataframe with the given day, tries, and user """
        entry = parse_message(message)
        if entry is None:
            return None

        # Dont duplicate entries
        if (
            (self.dataframe['day']   == entry.day)   &
            (self.dataframe['tries'] == entry.tries) &
            (self.dataframe['user']  == entry.user)
        ).any():
            return


        logging.info(f"Adding entry: {entry}")

        self.dataframe.loc[len(self.dataframe.index)] = [entry.day, entry.tries, entry.user]
        self.dataframe.to_csv(DF_PATH, index=False)

        return entry

    async def initial_populate(self):
        """ If dataframe doesnt exist, loop over all messages and scan for wordle results """
        for channel in utils.get_text_channels(self.bot):
            print("Scanning channel:", channel.name)
            async for message in channel.history(limit=None, oldest_first=True):
                self.update_dataframe(message)

        print("Finished initial population")

def format_leaderboard(dataframe: pd.DataFrame) -> str:
    stats = dataframe.groupby("user").describe()['tries'][['count', 'mean', 'min', 'std']]

    stats = stats.sort_values('mean').reset_index()
    stats.index += 1

    stats = stats.rename({'count': 'Entries', 'mean': 'Avg', 'min': 'Min', 'std': 'Stddev', 'user': 'User'}, axis=1)

    stats['Entries'] = stats['Entries'].astype(int)
    stats['Min'] = stats['Min'].astype(int)
    stats['User'] = stats['User'].apply(lambda x: x.split("#")[0])

    with pd.option_context('display.float_format', '{:0.2f}'.format):
        return stats.to_string()

def parse_message(message: Message) -> Optional[WordleResult]:
    split = re.split("(Wordle) (\d+) (\d\/\d)\n", message.content)
    if len(split) != 5:
        return None

    day   = int(split[2])
    tries = int(split[3].split("/")[0])

    user = f"{message.author.name}#{message.author.discriminator}"
    result = WordleResult(day=day, tries=tries, user=user)
    return result

def setup(bot):
    bot.add_cog(ChiiWordleBot(bot))
