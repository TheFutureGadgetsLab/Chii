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
from glicko2 import Player

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
        self.df: pd.DataFrame = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_dataframe()
        await self.scan_last_n_days(5)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        entry = self.update_dataframe(message)

        if entry is not None:
            await message.channel.send(f"Thanks for your submission, {entry.user}, you suck ass :)")

    @commands.command(name='wordle_leaderboard')
    async def leaderboard(self, ctx: Context) -> None:
        string = format_leaderboard(self.df, await self.glicko())
        string = f"```\n{string}```"
        await ctx.send(string)

    async def load_dataframe(self) -> None:
        """ Loads the dataframe from the csv file """

        if os.path.exists(DF_PATH):
            self.df = pd.read_csv(DF_PATH)
        else:
            self.df = pd.DataFrame(columns=["day", "tries", "user"])
            await self.initial_populate()

    def update_dataframe(self, message: Message) -> Optional[WordleResult]:
        """ Updates the dataframe with the given day, tries, and user """
        entry = parse_message(message)
        if entry is None:
            return None

        # Dont duplicate entries
        if (
            (self.df['day']   == entry.day)   &
            (self.df['tries'] == entry.tries) &
            (self.df['user']  == entry.user)
        ).any():
            return


        logging.info(f"Adding entry: {entry}")

        self.df.loc[len(self.df.index)] = [entry.day, entry.tries, entry.user]
        self.df.to_csv(DF_PATH, index=False)

        return entry

    async def initial_populate(self):
        """ If dataframe doesnt exist, loop over all messages and scan for wordle results """
        for channel in utils.get_text_channels(self.bot):
            print("Scanning channel:", channel.name)
            async for message in channel.history(limit=None, oldest_first=True):
                self.update_dataframe(message)

        print("Finished initial population")

    async def scan_last_n_days(self, days: int) -> None:
        logging.info("ChiiWordleBot: Scanning last %d days", days)
        import datetime 
        tod = datetime.datetime.now()
        d = datetime.timedelta(days=days)
        for channel in utils.get_text_channels(self.bot):
            async for message in channel.history(limit=None, oldest_first=True, after=tod-d):
                self.update_dataframe(message)

        logging.info("ChiiWordleBot: Finished scanning last %d days", days)

    async def glicko(self):
        def outcome(p1_tries, p2_tries):
            if p1_tries == p2_tries:
                return 0.5
            return int(p1_tries < p2_tries)

        users = self.df['user'].unique()
        players = {name:Player() for name in users}

        for day in range(self.df['day'].min(), self.df['day'].max()):
            subset = self.df[self.df['day'] == day]

            ratings = {}
            rds     = {}
            tries   = {}
            for name, player in players.items():
                if name not in subset['user'].values:
                    tries_ = 7
                else:
                    tries_ = subset[subset['user'] == name]['tries'].iloc[0]

                ratings[name] = players[name].rating
                rds[name]     = players[name].rd
                tries[name]   = tries_

            for name, player in players.items():
                player.update_player(
                    rating_list=[ratings[k] for k in ratings if k != name],
                    RD_list=[rds[k] for k in rds if k != name],
                    outcome_list=[outcome(tries[name], tries[k]) for k in ratings if k != name]
                )

        results = {k:v.rating for k,v in players.items()}
        results = {k:v for k,v in sorted(results.items(), key=lambda x: x[1])}
        return results

def format_leaderboard(dataframe: pd.DataFrame, glicko) -> str:
    stats = dataframe.groupby("user").describe()['tries'][['count', 'mean', 'min', 'std']]

    for name, elo in glicko.items():
        stats.loc[name, 'Elo'] = elo

    stats = stats.sort_values('Elo', ascending=False).reset_index()
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
