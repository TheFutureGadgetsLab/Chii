import os
import re
from collections import namedtuple
from typing import Tuple, Union

import discord
import pandas as pd
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

WordleResult = namedtuple('WordleResult', ['day', 'tries', 'user'])

DF_PATH = "data/wordle.csv"

class ChiiWordleBot(commands.Cog):
    """ 
    ChiiWordleBot is a discord bot that scans messages for wordle results and
    creates a leaderboard based on user performance
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()

        self.bot = bot

        # Stores results
        self.dataframe = None

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        result = self.try_parse_message(message)
        if result is None: # Failed to parse
            return

        await message.channel.send(f"Thanks for your submission, {result.user}, you suck ass :)")

    def try_parse_message(self, message: Message) -> Union[None, WordleResult]:
        split = re.split("(Wordle) (\d+) (\d\/\d)", message.content)
        if len(split) != 5:
            return None

        day   = int(split[2])
        tries = int(split[3].split("/")[0])

        user = f"{message.author.name}#{message.author.discriminator}"
        result = WordleResult(day=day, tries=tries, user=user)
        self.update_dataframe(result)

        return WordleResult(day=day, tries=tries, user=user)

    async def load_dataframe(self):
        """ Loads the dataframe from the csv file """

        if os.path.exists(DF_PATH):
            self.dataframe = pd.read_csv(DF_PATH)
        else:
            self.dataframe = pd.DataFrame(columns=["day", "tries", "user"])
            await self.initial_populate()
    
    def update_dataframe(self, result: WordleResult) -> bool:
        """ Updates the dataframe with the given day, tries, and user """

        # Dont duplicate entries
        if (
            (self.dataframe['day']   == result.day)   &
            (self.dataframe['tries'] == result.tries) &
            (self.dataframe['user']  == result.user)
        ).any():
            return

        self.dataframe.loc[len(self.dataframe.index)] = [result.day, result.tries, result.user]
        self.dataframe.to_csv(DF_PATH, index=False)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_dataframe()

    async def initial_populate(self):
        """ If dataframe doesnt exist, loop over all messages and scan for wordle results """
        for channel in self.bot.get_all_channels():
            try:
                await channel.history(limit=1, oldest_first=False)
            except:
                continue

            print("Scanning channel:", channel.name)
            async for message in channel.history(limit=None):
                self.try_parse_message(message)

        print("Finished initial population")

def setup(bot):
    bot.add_cog(ChiiWordleBot(bot))
