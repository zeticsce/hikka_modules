# Refactored by @morisummermods
# modded by @zeticsce
# meta developer: @zeticsce
# developer: @trololo_1
from .. import loader, utils  # noqa
import asyncio
import contextlib
import pytz
import re
import telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time


class DianaListMod(loader.Module):
    """Список заражений для дианы."""
    strings = {
        "name": "DianaList"
    }

    async def client_ready(self, client, db):
        self.db = db
        if not self.db.get("DianaNumMod", "DianaexUsers", False):
            self.db.set("DianaNumMod", "DiananexUsers", [])
        if not self.db.get("DianaNumMod", "DianainfList", False):
            self.db.set("DianaNumMod", "DianainfList", {})    

    async def зрcmd(self, message):
        """ Лист заражений дианы.\n.зар {@id/user} {count} {args}\nДля удаления: .зарр {@id/user}\nАргументы:\nк --
        добавить букву k(тысяч) к числу.\nф -- поиск по ид'у/юзеру.\nр -- добавлению в список по реплаю. """
        args = utils.get_args_raw(message)
        infList = self.db.get("DianaNumMod", "DianainfList")
        timezone = "Europe/Kiev"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        with contextlib.suppress(Exception):
            args_list = args.split(' ')
        if not args:
            if not infList:
                await utils.answer(message, "Лист заражений <b>пуст</b>.")
                return
            sms = ''.join(
                f'<b>• <code>{key}</code> -- <code>{value[0]}</code> [<i>{value[1]}</i>]</b>\n' for key, value in
                infList.items())
            await utils.answer(message, sms)
            return
        if 'р' in args.lower():
            reply = await message.get_reply_message()
            if not reply:
                return await utils.answer(message, 'Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
            elif reply.sender_id != 707693258 and 'подверг заражению' not in reply.text:
                return await utils.answer(message, 'Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
            else:  # ☣
                text = reply.text
                x = text.index('☣') + 4
                count = text[x:].split(' ', maxsplit=1)[0]
                x = text.index('user?id=') + 8
                user = '@' + text[x:].split('"', maxsplit=1)[0]
                infList[user] = [str(count), vremya]
                self.db.set("DianaNumMod", "DianainfList", infList)
                await utils.answer( 
                    message,
                    f"Жертва <code>{user}</code> добавлена.\n"
					
					
					f"Дата: <b>{vremya}</b>\n"
					f"☣️ <b>{count}</b> био-опыта."
                )
        elif args_list[0] == "clear":
            infList.clear()
            self.db.set("DianaNumMod", "DianainfList", infList)
            await utils.answer(message, "Лист заражений <b>очищен</b>.")
        elif args_list[0] in infList and 'ф' in args.lower():
            user = infList[args_list[0]]
            await utils.answer(message, f"<b>• <code>{args_list[0]}</code> -- ☣️ {user[0]}</b> [<i>{user[1]}</i>]")
        elif len(args_list) == 1 and args_list[0] in infList:
            infList.pop(args_list[0])
            self.db.set("DianaNumMod", "DianainfList", infList)
            await utils.answer(message, f"Пользователь <code>{args}</code> удалён из списка.")
        elif args_list[0][0] != '@':
            await utils.answer(message, 'Это не <b>@ид/юзер</b>.')
        else:
            try:
                user, count = str(args_list[0]), float(args_list[1])
            except Exception:
                await utils.answer(message, "Данные были введены не корректно")
                return
            k = ''
            if 'к' in args.lower():
                k += 'k'
            infList[user] = [str(count) + k, vremya]
            self.db.set("DianaNumMod", "DianainfList", infList)
            await utils.answer( 
                    message,
                    f"Жертва <code>{user}</code> добавлена.\n"
					
					
					f"Дата: <b>{vremya}</b>\n"
					f"☣️ <b>{count}</b>{k} био-опыта."
                )

