__version__ = (1, 7, 9)

#           ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
#           ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
#           ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
#           ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
#           ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
#           ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
#                                © Copyright 2022
#                             https://t.me/zeticsce
#               
#                   🔒         Licensed under the GNU AGPLv3
#                   🌐 https://www.gnu.org/licenses/agpl-3.0.html
# developer of Num: @trololo_1
# meta developer: @zeticsce
from .. import loader, utils  # noqa
import asyncio
import contextlib
import pytz
import re
import telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time
import logging
import types
logger = logging.getLogger(__name__)

@loader.tds
class BioMod(loader.Module):
    """Ваша вторая рука в биовойнах)"""
    strings = {
        "name": "🦠 Bio",
      # Notes and Notexec modules strings:
        "execute_fail": ("<b>Failed to execute expression:</b>\n<code>{}</code>"),
        "what_note": "<b>Какую заметку нужно показать?</b>",
        "no_note": "<b>Заметка не найдена</b>",
        "save_what": "<b>А что сохранить?</b>",
        "what_name": "<b>А как будет называться заметка?</b>",
        "saved": "<b>Заметка сохранена как:</b> <code>{}</code>",
        "notes_header": "<b>Сохранённые заметки:</b>\n\n",
        "notes_item": "<b>▷</b> <code>{}</code>",
        "delnote_args": "<b>А какую заметку нужно удалить?</b>",
        "delnote_done": "<b>Заметка удалена!</b>",
        "delnotes_none": "<b>А заметок-то нету...</b>",
        "delnotes_done": "<b>ВСЕ ЗАМЕТКИ УДАЛЕНЫ</b>",
        "notes_none": "<b>А заметок-то нету...</b>"
    }
    async def client_ready(self, client, db):
        self.db = db
        self.client = client #IDS
        if not self.db.get("NumMod", "exUsers", False):
            self.db.set("NumMod", "exUsers", [])
        if not self.db.get("NumMod", "infList", False):
            self.db.set("NumMod", "infList", {})
#### Module: IDS by @Not_Toxa
    async def actions(self, reply, args):
        if reply:
            user_id = reply.sender_id
            return {
                "user_id": user_id,
                "firstname": (
                    await self.client.get_entity(user_id)
                ).first_name
            }
        elif len(args) == 1:
            if args[0].isdigit():
                args[0] = int(args[0])
            entity = await self.client.get_entity(args[0])
            return {
                "user_id": entity.id,
                "firstname": entity.first_name
            }
    async def айcmd(self, message):
        """[@user/@id/linkID/reply]\nПолучает айди пользователя по реплаю и по тегу"""
        reply = await message.get_reply_message()
        vlad = message.sender_id
        args = utils.get_args(message)
        user_info = await self.actions(reply, args)
        if not isinstance(user_info, dict):
            return await utils.answer(
            message,
            "<b>My 🆔:</b> <code>@{}</code>".format(
                str(vlad)
            )
        )
        await utils.answer(
            message,
            "<b>🥷🏻</b> <a href='tg://openmessage?user_id={}'>{}</a>\n<b>🆔:</b> <code>@{}</code>".format(
                user_info["user_id"], user_info["firstname"], user_info["user_id"]
            )
        )
### Module Num by trololo_1
    async def зcmd(self, message):
        " [arg] [arg] [arg]....\n В качестве аргументов используй числа или первые символы строки."
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        count_st = 0
        count_hf = 0
        vladebi = reply.sender_id
        if not reply:
            await message.reply('❌ Нет реплая.')
            return
        args = utils.get_args_raw(message)
        list_args = []
        if not args:
            await message.reply(f'<code>/заразить 10 @{vladebi}<code>')
            await asyncio.sleep(1)
            await message.delete()
            return
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    list_args.extend(str(x) for x in range(int(ot_do[0]), int(ot_do[1]) + 1))
                except Exception:
                    await message.reply('❌ еблан, Используй правильно функцию "от-до".')
                    return
            else:
                list_args.append(i)
        a = reply.text
        lis = a.splitlines()
        for start in list_args:
            for x in lis:
                if x.lower().startswith(str(start.lower())):
                    count_st = 1
                    if 'href="' in x:
                        count_hf = 1
                        b = x.find('href="') + 6
                        c = x.find('">')
                        link = x[b:c]
                        if link.startswith('tg'):
                            users = '@' + link.split('=')[1]
                            if users in exlist:
                                await message.reply(f'❎ Исключение: <code>{users}</code>')
                            else:
                                await message.reply(f'/заразить {users}')
                        elif link.startswith('https://t.me'):
                            a = '@' + str(link.split('/')[3])
                            if a in exlist:
                                await message.reply(f'❎ Исключение: <code>{a}</code>')
                            else:
                                await message.reply(f'/заразить {a}')
                        else:
                            await message.reply('🤔 Что за хуета?')
                        break
            await asyncio.sleep(3)   
        if not count_st:
            await message.reply('❌ Не найдено совпадение в начале строк с аргументами.')
        elif not count_hf:
            await message.reply('❌ Ссылка не найдена.')
        elif len(list_args) >= 5:
            await message.reply('✅ Заражения завершены.')
    async def оcmd(self, message):
        """Заражает всех по реплаю.\nИспользуй ответ на сообщение с @id/@user/link"""
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        if not reply:
            await message.edit('❌ Нет реплая.')
            return
        json = JSON.loads(reply.to_json())
        for i in range(len(reply.entities)):
            try:
                link = json["entities"][i]["url"]
                if link.startswith('tg'):
                    users = '@' + link.split('=')[1]
                    if users in exlist:
                        await message.reply(f'❎ Исключение: <code>{users}</code>')
                    else:
                        await message.reply(f'/заразить {users}')
                elif link.startswith('https://t.me'):
                    a = '@' 
                    if a in exlist:
                        await message.reply(f'❎ Исключение: <code>{a}</code>')
                    else:
                        await message.reply(f'/заразить {a}')
                else:
                    await message.reply('🤔 Что за хуета?')
            except Exception:
                await message.reply("/заразить " + reply.raw_text[
                                                  json["entities"][i]["offset"]:json["entities"][i]["offset"] +
                                                                                json["entities"][i]["length"]])
            await asyncio.sleep(3)
        await message.delete()
    async def искcmd(self, message):
        """Добавляет исключения для команд .з и .о\nИспользуй: .иск {@user/@id}"""
        args = utils.get_args_raw(message)
        exlistGet = self.db.get("NumMod", "exUsers")
        exlist = exlistGet.copy()
        if not args:
            if len(exlist) < 1:
                await message.edit('❌ Cписок исключений пуст.')
                return
            exsms = ''.join(f'<b>{count}.</b> <code>{i}</code>\n' for count, i in enumerate(exlist, start=1))
            await utils.answer(message, exsms)
            return
        #if reply:
        if args == 'clear':
            exlist.clear()
            self.db.set("NumMod", "exUsers", exlist)
            await message.respond(' ❎ Список исключений очищен.')
            return
        if len(args.split(' ')) > 1 or args[0] != '@':
            await message.respond(
                '❌ Кол-во аргументов <b>больше</b> одного, либо начинается <b>не</b> со знака <code>@</code>'
            )
            return
        if args in exlist:
            exlist.remove(args)
            self.db.set("NumMod", "exUsers", exlist)
            await message.edit(f'❎ Пользователь <code>{args}</code> исключен.')
            return
        exlist.append(args)
        self.db.set("NumMod", "exUsers", exlist)
        await message.edit(f'✅ Пользователь <code>{args}</code> в исключениях.')
    async def зарcmd(self, message):
        """ Список ваших заражений.\n.зар {@id/user} {count} {args}\nДля удаления: .зар {@id/user}\nАргументы:\nк -- добавить букву k(тысяч) к числу.\nф -- поиск по ид'у/юзеру.\nр -- добавлению в список по реплаю. """
        args = utils.get_args_raw(message)
        infList = self.db.get("NumMod", "infList")
        timezone = "Europe/Kiev"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        with contextlib.suppress(Exception):
            args_list = args.split(' ')
        if not args:
            if not infList:
                await utils.answer(message, "❌ Список заражений пуст.")
                return
            sms = ''.join(
                f'<b>• <code>{key}</code>  <code>{value[0]}</code> [<i>{value[1]}</i>]</b>\n' for key, value in
                infList.items())
            await utils.answer(message, sms)
            return
        if 'р' in args.lower():
            reply = await message.get_reply_message()
            text = reply.text
            if not reply:
                return await utils.answer(message, '❌ Нет реплая на сообщение ириса о заражении.')
            elif reply.sender_id != 707693258 and 'Заражение на' not in reply.text:
                return await utils.answer(message, '❌ Реплай <b>не</b> на сообщение ириса о заражении "<b>...подверг заражению...</b>"')
            else:  # ☣
                text = reply.text
                x = text.index('☣') + 4
                count = text[x:].split(' ', maxsplit=1)[0]
                x = text.index('user?id=') + 8
                user = '@' + text[x:].split('"', maxsplit=1)[0]
                infList[user] = [str(count), vremya]
                self.db.set("NumMod", "infList", infList)
                await utils.answer(
                    message,
                    f"✅ Жертва <b><code>{user}</code></b> сохранена.\n"
                    f"<b>☣️ {count}</b> био-опыта."
                )
        elif args_list[0] == "clear":
            infList.clear()
            self.db.set("NumMod", "infList", infList)
            await utils.answer(
                message,
            f"✅ Зарлист <b>очищен</b>."
            )
        elif args_list[0] in infList and 'ф' in args.lower():
            user = infList[args_list[0]]
            await utils.answer(message,
                f"✅ Жертва <code>{args_list[0]}</code> приносит:\n"
                f"<b>☣️ {user[0]} био-опыта.</b>\n"
                f"📆 Дата: <i>{user[1]}</i>"
            )
        elif len(args_list) == 1 and args_list[0] in infList:
            infList.pop(args_list[0])
            self.db.set("NumMod", "infList", infList)
            await utils.answer(
                message, 
                f"❌ Жертва <b><code>{args}</code></b> удалена из списка."
            )
        elif args_list[0][0] != '@':
            await utils.answer(message,
            f'🥱 Вы некорректно ввели ID.'
            )
        else:
            try:
                user, count = str(args_list[0]), float(args_list[1])
            except Exception:
                await utils.answer(message, 
                    f"❎ Данного пользователя нет в списке."
                    )
                return
            k = ''
            if 'к' in args.lower():
                k += 'k'
            infList[user] = [str(count) + k, vremya]
            self.db.set("NumMod", "infList", infList)
            await utils.answer(
                message,
                f"✅ Жертва <b><code>{user}</code></b> сохранена.\n"
                f"<b>☣️ {count}{k}</b> био-опыта."
            )
    async def довcmd(self, message):
        """ {args1} {args2 OR reply} \nВведи команду для просмотра аргументов."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        if not args:
            return await utils.answer(
                message,
                f""
                f"<b>🌘 <code>.Дов сет</code> <id|реплай></b> --- Добавить/удалить саппорта (не больше 20).\n"
                f"[{', '.join([f'<code>@{i}</code>' for i in filter_and_users['users']])}]\n"
                f"<b><code>🌘 .Дов ник</code> <ник></b> --- <b>Установить ник</b>.\n<i>Например: <b><code>.Дов ник </i></code>Влад</b></i>.\n"
                f"<b>🔰 Ваш ник: <code>{filter_and_users['filter'] or '❌ Не установлен.'}</code></b>\n"
                f"<b><code>🌘 .Дов пуск</code></b> --- <b>Запустить/Остановить</b>.\n"
                f"<b>{'✅ Запущен.' if filter_and_users['status'] else '❌ Остановлен.'}.</b>\n\n"
                f"<b>❔ Как использовать:</b>\n"
                f"<b><ник></b> <code>бей</code></b> | <b><code>кус</code></b>ьай |<b><code>зарази</code></b>ть " # 🔽
                f"| <b><code>еб</code></b>и | <b><code>уеби</code></b> <b>(1-10) <Ссылка/реплай></b>.\n"
                f"<b><ник> <code><b>Вакцин</b></code>ау | <code><b>лечись</code></b> |" # 🔽
                f"<code><b>ва</code></b>кцина</b> | <code><b>хи</code></b>лльсяйинг\n"
                f"<b><ник></b> <code>жертвы</code> | <code>ежа</code><b>\n"
                f"<b><ник> </b><code>бол</code>езни\n"
                f"<b><ник> </b><code>цен</code>аз\n"
                f"<b><ник> </b><code>лаб</code>уа | <code>статы</code>\n"
                f"<b><ник> </b><code>уведы</code>\n"
                f"<b><ник> </b><code>-вирусы</code>\n\n"
                f"<b>〽️ Апгрейд навыков:</b>\n"
                f"<b><ник> <навык> (0-5)</b> или\n<b><ник> <навык> чек (0-5)</b>\n"
                f"<i>Например: <b><ник> квалификация 4</b>\n" 
                f"(улучшает квалификацию учённых на 4 ур.)</i>\n\n"    
                f"<b>〽️ Доступные навыки:</b>\n"
                f"<b>🧪 <code>Патоген</code> (паты)</b>\n<b>👨‍🔬 <code>Квалификация</code> (квала)</b>\n"
                f"<b>🦠 <code>Заразность</code> (зз)</b>\n<b>🛡 <code>Иммунитет</code> (иммун)</b>\n"
                f"<b>☠️ <code>Летальность</code> (летал)</b>\n<b>🕵️‍♂️ <code>Безопасность</code> (сб)</b>"
            )
        args = args.split(' ', maxsplit=1)
        if len(args) == 1 and not reply and args[0] != 'пуск': # 
            return await utils.answer(message, '🤔 Не могу понять, что за хуета?..')
        elif args[0] == 'сет':
            try:
                user_id = args[1]
                if not user_id.isdigit():
                    return await utils.answer(message, '👀 Правильно 🆔 введи, дубина.')
            except Exception:
                user_id = str(reply.sender_id)
            if user_id in filter_and_users['users']:
                filter_and_users['users'].remove(user_id)
                await utils.answer(message, f"❎ Саппорт <b><code>{user_id}</code></b> удалён.")
            elif len(filter_and_users['users']) <= 20:
                filter_and_users['users'].append(user_id)
                await utils.answer(message, f"✅ Саппорт <b><code>{user_id}</code></b> добавлен!")
            else:
                return await utils.answer(message, '❌ Превышен лимит в 20 человек.')
            return self.db.set("NumMod", "numfilter", filter_and_users)
        elif args[0] == 'ник':
            try:
                filter_and_users['filter'] = args[1].lower().strip()
                self.db.set("NumMod", "numfilter", filter_and_users)
                return await utils.answer(message, f"✅ Ник <b><code>{args[1]}</code></b> успешно установлен!")
            except Exception:
                return await utils.answer(message, "<b>📝 Введите ник.</b>")
        elif args[0] == 'пуск':
            if filter_and_users['status']:
                filter_and_users['status'] = False
                self.db.set("NumMod", "numfilter", filter_and_users)
                return await utils.answer(message, "<b>❎ Успешно остановлено.</b>")
            else:
                filter_and_users['status'] = True
                self.db.set("NumMod", "numfilter", filter_and_users)
                return await utils.answer(message, "<b>✅ Успешно запущено!</b>")
        else:
            return await utils.answer(
            message,
            f"<b>❌ Неизвестный аргумент.</b>\n"
            f"<i>📝 Введите <code>.дов</code> для просмотра команд.</i>"
            )
    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        user_id = str(message.sender_id)
        if not filter_and_users['filter'] or not filter_and_users['status'] or user_id not in filter_and_users[
            'users'] or message.is_private: return
        text = message.raw_text.lower()
        if not text.startswith(filter_and_users['filter']): return
        if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?(?P<link>@[0-9a-z_]+|(?:https?://)?t\.me/[0-9a-z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))",
                text):
            send_mesа = send_mesа.groupdict()
            send_mesа['link'], send_mesа['id'] = '@' + send_mesа['id'] if send_mesа['id'] else send_mesа['link'], ''
            send_mesа['z'] = '/заразить '
            send_mesа['lvl'] = send_mesа['lvl'] or ''
            mes = ''.join(send_mesа.values())
            await message.reply(mes)
####### чеки
        elif send_mes := re.search(r"(?P<ch>зараз[уканость]{,5} чек[айниуть]{,4}\s|зз чек[айниуть]{,4}\s|чек[ниуть]{,4} зз\s|чек[айниуть]{,4} зараз[куаность]{,5}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['ch'] = '+заразность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<pat>пат[огены]{,5} чек[айниуть]\s|чек[айниуть]{,4} пат[огены]{,5}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['pat'] = '+патоген '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<let>летал[каьностьу]{,5} чек[айниуть]{,4}\s|чек[айниуть]{,4} летал[каьностьу]{,5}\s)(?P<lvl>[1-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['let'] = '+летальность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<kvala>квал[лаификацияу]{,8} чек[айниуть]{,4}\s|разраб[откау]{,4} чек[айниуть]{,4}\s|чек[айниуть]{,4} разраб[откау]{,4}\s|чек[айниуть]{,4} квал[улаификация]{,8}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['kvala'] = '+квалификация '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<imun>чек[айниуть]{,4} иммун[еитеткау]{,4}\s|чек[айниуть]{,4} имун[еитеткау]{,4}\s|имун[еитеткау]{,4} чек[айниуть]{,4}\s|иммун[еитеткау]{,4} чек[айниуть]{,4}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['imun'] = '+иммунитет '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<sb>сб чек[айниуть]{,4}\s|безопасно[сть]{,3} чек[айниуть]{,4}\s|служб[ау]{,2} чек[айниуть]{,4}\s|служб[ау]{,2} безопасно[стиь] чек[айниуть]{,4}|чек[айниуть]{,4} служб[ау]{,2} безопасно[стиь]\s|чек[айниуть]{,4} служб[ау]{,2}\s|чек[айниуть]{,4} безопасно[сть]{,3}\s|чек[айниуть]{,4} сб\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['sb'] = '+безопасность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<zar>зараз[уканость]{,5}\s|зз\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['zar'] = '++заразность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<pat>пат[огены]{,5}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['pat'] = '++патоген '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<let>летал[укаьность]{,5}\s)(?P<lvl>[1-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['let'] = '++летальность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<kvala>квал[улаификация]{,8}\s|разраб[откау]{,4}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['kvala'] = '++квалификация '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<imun>иммун[уеитетка]{,4}|имун[уеитетка]{,4}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['imun'] = '++иммунитет '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        elif send_mes := re.search(r"(?P<sb>сб\s|безопасно[сть]{,3}\s|служб[ау]{,2} безопасно[стиь]{,3}\s)(?P<lvl>[0-5]+)", text):
            send_mes = send_mes.groupdict()
            send_mes['sb'] = '++безопасность '
            send_mes['lvl'] = send_mes['lvl'] or ''
            mes = ''.join(send_mes.values())
            await message.reply(mes)
        if re.search(r"бол[езьни]{,2}", text):
            await message.reply('/мои болезни')
        if re.search(r"жертв[ыау]{,2}|еж[а]{,2}", text):
            await message.reply('/мои жертвы')
        if re.search(r"стат[ыа]{,2}|лаб[уа]{,2}", text):
            await message.reply('/лаю')
        if re.search(r"цен[аз]{,2}", text):
            await message.reply('купить вакцину')
        if re.search(r"увед[ыаомления]{,2}", text):
            await message.reply('+вирусы')
        if re.search(r"-вирус[ыа]{,2}", text):
            await message.respond('-вирусы')
        elif re.search(r"вак[цинау]{,2}|лечись|хи[лльсяйинг]{,2}", text):
            await message.respond('/купить вакцину')
###     
    async def гcmd(self, message):
        " [arg] [arg] [arg]....\nВыполняет команду /ид по реплаю\n Аргументом являются числа и первые символы строки. "
        reply = await message.get_reply_message()
        a = reply.text
        count_st = 0
        count_hf = 0
        if not reply:
            await message.respond('❌ Нет реплая.')
            return
        args = utils.get_args_raw(message)
        list_args=[]
        if not args:
            await message.edit('❌ Нет аргументов')
            return
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    for x in range(int(ot_do[0]),int(ot_do[1])+1):
                        list_args.append(str(x))
                except:
                    await message.respond('❌ Используй правильно функцию "от-до".')
                    return
            else:
                list_args.append(i)
        lis = []
        for i in a.splitlines():
            lis.append(i)
        for start in list_args:
            for x in lis:
                if x.lower().startswith(str(start.lower())):
                    count_st = 1
                    if 'href="' in x:
                        count_hf = 1
                        b=x.find('href="')+6
                        c=x.find('">')
                        link = x[b:c]
                        if link.startswith('tg'):
                            list = []
                            for i in link.split('='):
                                list.append(i)
                            await message.reply(f'/id <code>@{list[1]}</code>'
                            )
                            break
                        elif link.startswith('https://t.me'):
                            a ='@' + str(link.split('/')[3])
                            await message.reply(f'/id <code>{a}</code>'
                            )
                            break
                        else:
                            await message.reply('🤔 Что за хуета?')
                            break
            await asyncio.sleep(3)
        if not count_st:
            await message.edit('❌ Не найдено совпадение в начале строк с аргументами.')
        elif not count_hf:
            await message.edit('❌ Ссылка не найдена.')
        elif len(list_args) >= 3:
            await message.respond("<b>✅ Id'ы успешно извлечены.</b>" )
            await asyncio.sleep(3)
    async def иcmd(self, message):
        "Чекает все айди по реплаю."
        reply = await message.get_reply_message()
        json = JSON.loads(reply.to_json())
        for i in range(0, len(reply.entities) ):
            try:
                link = json["entities"][i]["url"]
                if link.startswith('tg'):
                    list = []
                    for i in link.split('='):
                        list.append(i)
                    await message.reply('/id <code>@' + list[1] + '</code>')
                elif link.startswith('https://t.me'):
                    a ='@' + str(link.split('/')[3])
                    await message.reply(f'/id <code>{a}</code>')
                else:
                    await message.reply('🤔 Что за хуета?')
            except:
                await message.reply("/id " + "<code>" + reply.raw_text[json["entities"][i]["offset"]:json["entities"][i]["offset"]+json["entities"][i]["length"]] + "</code>" )
            await asyncio.sleep(3)
        await message.delete()



































































































































