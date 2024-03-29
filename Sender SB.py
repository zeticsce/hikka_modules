# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# developer: @D4n13l3k00
# meta developer: @zeticsce


import re

from telethon.errors import ChannelInvalidError

from .. import loader, utils
import asyncio


@loader.tds
class SenderSBMod(loader.Module):
    strings = {"name": "SenderSB"}

    @loader.owner
    async def snddcmd(self, m):
        """.snd <канал/чат/id> <reply>
        Отправить сообшение в чат/канал(без авторства)
        """
        args = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if not args:
            return await m.edit("[Sender] Укажите канал/чат")
        try:
            this = await m.client.get_input_entity(
                int(args) if re.match(r"-{0,1}\d+", args) else args
            )
        except ChannelInvalidError as e:
            return await m.edit("[Sender] Такого канала/чата не существует!")
        except Exception as e:
            return await m.edit("[Sender] Неизвестная мне ошибка:\n" + " ".join(e.args))
        await asyncio.sleep(60)
        await m.client.send_message(this, reply)
        await m.delete()