import random

import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot

from src.CogSkeleton import CogSkeleton


class ChiiPresenceCog(CogSkeleton):
    CHOICES = [
        discord.Activity(type=discord.ActivityType.watching,  name="Benson"),
        discord.Activity(type=discord.ActivityType.competing, name="the Bot Olympics"),
        discord.Activity(type=discord.ActivityType.listening, name="Jordan Peterson"),
    ]

    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.change_presence.start()
        self.is_ready = False 

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_ready = True
        await self.bot.change_presence(activity=random.choice(self.CHOICES))

    @tasks.loop(hours=4)
    async def change_presence(self):
        if not self.is_ready:
            return

        choice = random.choice(self.CHOICES)
        self.logger.info(f"Changing presence to {choice}!")

        await self.bot.change_presence(activity=choice)

    def cog_unload(self):
        self.change_presence.cancel()

def setup(bot):
    bot.add_cog(ChiiPresenceCog(bot))
