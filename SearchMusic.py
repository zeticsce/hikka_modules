# ---------------------------------------------------------------------------------
#  ,_     _          
#  |\_,-~/          
#  / _  _ |    ,--.  🌐 This module was loaded through https://t.me/hikkamods_bot
# (  @  @ )   / ,-'  🔓 Not licensed.
#  \  _T_/-._( (     
#  /         `. \    ⚠️ Owner of this bot doesn't take responsibility for any
# |         _  \ |   errors caused by this module or this module being non-working
#  \ \ ,  /      |   and doesn't take ownership of any copyrighted material.
#   || |-_\__   /    
#  ((_/`(____,-'     
# ---------------------------------------------------------------------------------
# Name: SearchMusic
# Description: Модуль SearchMusic - поиск музыки
# Работает через бота @lybot
# Author: SekaiYoneya
# Commands:
# .sm
# ---------------------------------------------------------------------------------

# @Sekai_Yoneya

from .. import loader, utils


@loader.tds
class SearchMusicMod(loader.Module):
    """
    Модуль SearchMusic - поиск музыки
    Работает через бота @lybot
    """

    strings = {"name": "SearchMusic"}

    async def smcmd(self, message):
        """Используй: .sm «название» чтобы найти музыку по названию."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.reply("<b>Нету аргументов.</b>")
        try:
            await message.reply("<b>Загрузка...</b>")
            music = await message.client.inline_query("lybot", args)
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b>Музыка с названием <code>{args}</code> не найдена.</b>",
            )