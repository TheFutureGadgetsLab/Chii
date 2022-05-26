from random import random
from typing import Callable

from discord.ext import commands
from discord.message import Message

class Hook:
    def __init__(self, 
        hook_func: Callable,
        condition: Callable,
        ignore_bot: bool = True,
        with_prob: float = 1.0,
    ):
        self.hook_func  = hook_func
        self.condition  = condition

        self.ignore_bot = ignore_bot
        self.with_prob  = with_prob

    def cond_met(self, message: Message) -> bool:
        if self.ignore_bot and message.author.bot:
            return False

        return self.condition(message) and random() < self.with_prob
    
class HookLimb:
    def register_hook(self,
        hook_func: Callable,
        condition: Callable = lambda message: True,
        ignore_bot: bool = True,
        with_prob: float = 1.0,

    ) -> None:
        self.hooks.append(Hook(hook_func, condition, ignore_bot, with_prob))

    async def process_hooks(self, message: Message) -> None:
        for hook in self.hooks:
            if hook.cond_met(message):
                await hook.hook_func(message)