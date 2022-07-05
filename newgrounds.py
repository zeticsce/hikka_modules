__version__ = (1, 0, 0)
"""
    █▀▄▀█ █▀█ █▀█ █ █▀ █ █ █▀▄▀█ █▀▄▀█ █▀▀ █▀█
    █ ▀ █ █▄█ █▀▄ █ ▄█ █▄█ █ ▀ █ █ ▀ █ ██▄ █▀▄
    Copyright 2022 t.me/morisummermods
    Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: inline_content
# requires: requests
# meta developer: @morisummermods

from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
from ..inline.types import InlineQuery
from ..utils import rand
from .. import loader  # noqa
from .. import utils  # noqa
import logging
import requests
import io
import re

logger = logging.getLogger(__name__)
url = r"https://www.newgrounds.com/audio/listen/"


class NewGroundsMod(loader.Module):
    """Поиск песен с newgrounds.com"""

    id = 0
    strings = {
        "name": "newgrounds",
        "author": "morisummermods",
    }

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        try:
            channel = await self.client.get_entity(f"t.me/{self.strings['author']}")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.info(f"Can't join {self.strings['author']}")
        # try:
        #     post = (await client.get_messages(self.strings["author"], ids=[self.id]))[0]
        #     await post.react("❤️")
        # except Exception:
        #     logger.info(f"Can't react to t.me/{self.strings['author']}")

    async def ngcmd(self, message: Message) -> None:
        """Найти песню по id"""
        song_id = utils.get_args_raw(message)
        if not song_id or not song_id.isdigit():
            return await utils.answer(message, "<b>🔢 Введите корректный ID</b>")
        msg = await utils.answer(message, "<b>🔎 Поиск...</b>")
        response = await utils.run_sync(requests.get, f"{url}{song_id}")
        if response.status_code != 200:
            return await msg.edit(
                f"<b>🔦 Ошибка, не найдено <code>{response.status_code}</code></b>",
            )
        song_url = re.findall(
            r"new embedController\(\[\{\"url\":\"(.*)\",\"is",
            response.text
        )[0].replace("\\", "")
        artist = re.findall(r"\.com\">(.*?)</a>", response.text)[1].strip()
        title = re.findall(r"itemprop=\"name\">(.*)</", response.text)[0].strip()
        song = io.BytesIO((await utils.run_sync(requests.get, song_url)).content)
        song.name = f"{artist} - {title}.mp3"
        await utils.answer(
            message,
            song,
            caption=f"<b>🎶 {artist} - {title} (ID: <code>{song_id}</code>)</b>",
            asfile=True,
        )