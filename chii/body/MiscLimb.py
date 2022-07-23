import io
from random import random
from typing import List

import imageio.v3 as iio
import numpy as np
from discord import Embed, File
from discord.channel import TextChannel
from discord.message import Message
from typing import Optional


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

    def find_image_in_message(self, msg: Message) -> Optional[str]:
        """ Locates an image or video in a message, returning the URL. """

        for embed in msg.embeds:
            if embed.image != Embed.Empty:
                return embed.image.url
            if embed.video != Embed.Empty:
                return embed.video.url
        
        for attach in msg.attachments:
            if attach.content_type.split("/")[0] in ["image", "video"]:
                return attach.url

        return None

    def image_file_from_array(self, img: np.array, fname: str, extension: str) -> File:
        """ Converts np array image/video to a discord file 
            
            Args:
                img: np array image/video
                fname: filename without extension
                extension: file extension without period
        """

        extension = f".{extension}"
        fname = f"{fname}{extension}"

        bytes_image = iio.imwrite("<bytes>", img, extension=extension)
        byte_stream = io.BytesIO(bytes_image)
        return File(byte_stream, filename=fname)
