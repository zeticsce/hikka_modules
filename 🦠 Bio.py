__version__ = (2, 1, 0)

#           ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
#           ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
#           ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
#           ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
#           ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
#           ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
#                              НЕ © Copyright 2022
#                             https://t.me/zeticsce              


# developer of Num: @trololo_1
# meta developer: @zeticsce
from .. import loader, utils  # noqa
import asyncio
import contextlib
import pytz
import re
import telethon
from telethon.tl.types import MessageEntityTextUrl, Message
from telethon.tl.functions.users import GetFullUserRequest
import json as JSON
from telethon.errors.rpcerrorlist import FloodWaitError
from datetime import datetime, date, time
import logging
import types
from ..inline.types import InlineCall

@loader.tds
class BioMod(loader.Module):
    """Ваша вторая рука в биовойнах)"""
    strings = {
        
        "name": "Bio",
        
        "not_reply": "<emoji document_id=5215273032553078755>❌</emoji> Нет реплая.",
        
        "not_args": "<emoji document_id=5215273032553078755>❌</emoji> Нет аргументов.",
        
        "nolink": "<emoji document_id=5197248832928227386>😢</emoji> Нет ссылки на жертву.",

        "hueta": "🤔 Что за хуета?",
        
        "r.save":   
            "<emoji document_id=5212932275376759608>🦠</emoji> Жертва <b><code>{}</code></b> сохранена.\n"
            "<b>☣️ +{}{}</b> био-опыта.",
        
        "search":
            "<emoji document_id=5212932275376759608>✅</emoji> Жертва <code>{}</code> приносит:\n"
            "<b>☣️ +{} био-опыта.</b>\n"
            "📆 Дата: <i>{}</i>",
        
        "nf": "<emoji document_id=5215273032553078755>❎</emoji> Жертва не найдена.",
        
        "no_user": "<emoji document_id=5215273032553078755>❎</emoji> user {} don't exist.",

        "nous": "<emoji document_id=5215273032553078755>❎</emoji> Жертва или пользователь не существует.",

        "anf": "<emoji document_id=5215329773366025981>🤔</emoji> а кого искать?..",

        "aicmd":
            "<b>🥷🏻</b> <a href='tg://openmessage?user_id={}'>{}</a>\n"
            "<b>🆔:</b> <code>@{}</code>",
        "myid": "<b>My 🆔:</b> <code>@{}</code>",
        

        "guidedov":    
            "<b>❔ Как использовать доверку:</b>\n"
            "\n<b>{0}</b>  <code>бей</code> | <code>кус</code>[ьайни] | <code>зарази</code>[тьть] " # 🔽
            "| <code>еб</code>[ниажшь] | <code>уеб</code>[жиаошть] [1-10] (@id|@user|link)"
            "\n<b>{0}</b>  <code>цен</code>[ау] | <code>вч</code>[ек]  <i>(цена вакцины)</i>"
            "\n<b>{0}</b>  <code>вак</code>[цинау] | <code>леч</code>[ись] | <code>хи</code>[лльсяйинг] | <code>лек</code>[арство]"
            "\n<b>{0}</b>  <code>жертв</code>[ыау] | <code>еж</code>[ау]"
            "\n<b>{0}</b>  <code>бол</code>[езьни]"
            "\n<b>{0}</b>  <code>#лаб</code>[уа] | <code>%лаб</code>[уа] | <code>/лаб</code>[уа]"
            "\n<b>{0}</b>  <code>увед</code>[ыаомления]  <i>(+вирусы)</i>"
            "\n<b>{0}</b>  <code>-вирус</code>[ыа]\n\n"
            "〽️ <b>Апгрейд навыков:</b>\n"
            "<b>{0}  навык (0-5)</b> или\n<b>{0}  чек навык (0-5)</b>\n"
            "<i> Например: <b>{0} квалификация 4</b>\n" 
            "(улучшает квалификацию учённых на 4 ур.)</i>\n\n"    
            "〽️ <b>Доступные навыки:</b>\n"
            "🧪 Патоген (<b>пат</b> [огены])\n👨‍🔬 Квалификация (<b>квал</b> [ификацияула] | <b>разраб</b> [откау])\n"
            "🦠 Заразность (<b>зз</b> | <b>зараз</b> [аностьку])\n🛡 Иммунитет (<b>иммун</b> [итеткау])\n"
            "☠️ Летальность (<b>летал</b> [ьностькау])\n🕵️‍♂️ Безопасность (<b>сб</b> | <b>служб</b> [ау] | <b>безопасно</b> [сть])\n\n"
            "<b>🔎 Поиск жертв в зарлисте:</b>\n"
            "<b>{0}  зз [ @id ]</b> или\n"
            "<b>{0}  ж [ реплай ]</b>"
            "                см. <code>{1}config bio</code>",

        "dov": 
            "<b>🌘 <code>{5}Дов сет</code> [ id|реплай ]</b> --- <b>Добавить/удалить саппорта.</b>\n"
            "<i>   ✨ Доверенные пользователи:</i>\n"
            "{0}\n\n"
            "<b>🌘 <code>{5}Дов ник</code> ник</b> --- <b>Установить ник</b>.\n <i>Например: <b><code>.Дов ник {3}</code></b></i>.\n"
            "<b>   🔰 Ваш ник: <code>{1}</code></b>\n\n"
            "<b>🌘 <code>{5}Дов пуск</code></b> --- <b>Запустить/Остановить</b>.\n"
            "<b>   {2}</b>\n"
            "<i><b>Доступ открыт к:</b></i>\n{4}",

        "user_rm": "❎ Саппорт <b><code>{}</code></b> удалён.",
        "user_add": "<emoji document_id=5212932275376759608>✅</emoji> Саппорт <b><code>{}</code></b> добавлен!",
        "wrong_nick": "<b>📝 Введите ник.</b>",
        "nick_add": "🔰 Ник <b>{}</b> установлен!",
        "dov_start": "<b><emoji document_id=5212932275376759608>✅</emoji> Успешно запущено!</b>",
        "dov_stop": "<b>❎ Успешно остановлено.</b>",
        "dov.wrong_args": 
            "<b><emoji document_id=5215273032553078755>❌</emoji> Неизвестный аргумент.</b>\n"
            "<i>📝 Введите <code>.дов</code> для просмотра команд.</i>",   
        "wrong_id": "👀 Правильно 🆔 введи, дубина.",
        "ex": "❎ Исключение: <code>{}</code>",
        "wrong_ot-do": '<emoji document_id=5215273032553078755>❌</emoji> еблан, Используй <b>правильно</b> функцию "от-до".',
        "no_sargs": "<emoji document_id=5215273032553078755>❌</emoji> Не найдено совпадение в начале строк с аргументами.",
        "no_link": "<emoji document_id=5215273032553078755>❌</emoji> Ссылка не найдена.",
        "too_much_args": "<emoji document_id=5215273032553078755>❌</emoji> Кол-во аргументов <b>больше</b> одного, либо начинается <b>не</b> со знака <code>@</code>",
        "no_zar_reply": "<emoji document_id=5215273032553078755>❌</emoji> Нет реплая на сообщение ириса о заражении.",
        "empty_zar": "<emoji document_id=5215273032553078755>❌</emoji> Список заражений пуст.",
        "wrong_zar_reply": '<emoji document_id=5215273032553078755>❌</emoji> Реплай <b>не</b> на сообщение ириса о заражении "<b>...подверг заражению...</b>"',
        "wrong_cmd": "<emoji document_id=5215273032553078755>❌</emoji> Команда введена некорректно.",
        "empty_ex": "<emoji document_id=5215273032553078755>❌</emoji> Cписок исключений пуст.",
        "tids": "<b><emoji document_id=5212932275376759608>✅</emoji> Id'ы успешно извлечены.</b>",
        "tzar": "<emoji document_id=5212932275376759608>✅</emoji> Заражения завершены.",
        "clrex": "❎ Список исключений очищен.",
        "zar_rm": "❎ Жертва <b><code>{}</code></b> удалена из списка.",
        "exadd": "✅ Пользователь <code>{}</code> в исключениях.",
        "exrm": "❎ Пользователь <code>{}</code> удален.",
        "clrzar": "✅ Зарлист <b>очищен</b>.",
        "guide":
            "<b>Помощь по модулю BioHelper:</b>\n\n"
            "<code>{}biohelp дов</code> 👈 Помощь по доверке"

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
        """[reply]\nПолучает айди пользователя по реплаю."""
        reply = await message.get_reply_message()
        vlad = message.sender_id
        args = utils.get_args(message)
        user_info = await self.actions(reply, args)
        if not reply:
            return await message.edit(
                self.strings("myid").format(
                    vlad
                )
            )
        await message.edit(
            self.strings("aicmd").format(
                user_info["user_id"], user_info["firstname"], user_info["user_id"]
            )
        )
### Module Num by trololo_1
    async def зcmd(self, message):
        " [arg] [arg] [arg]....\n В качестве аргументов используй числа или первые символы строки.\n(без них бьет по ответу с 10 патов)"
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        count_st = 0
        count_hf = 0
        
        if not reply or not reply and not args:
            await message.reply(
                self.strings("not_reply")
            )
            return
        
        
        list_args = []
        args = utils.get_args_raw(message)
        if not args:
            vlad = reply.sender_id
            await message.reply(
                f'<code>/заразить 10 @{vlad}<code>\nспасибо <emoji document_id=5215327827745839526>❤️</emoji>'
            )
            return
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    list_args.extend(str(x) for x in range(int(ot_do[0]), int(ot_do[1]) + 1))
                except Exception:
                    await message.reply(
                        self.strings("wrong_ot-do")
                    )
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
                                await message.reply(
                                    self.strings("ex").format(
                                    users
                                    )
                                )
                            else:
                                await message.reply(f'/заразить {users}')
                        elif link.startswith('https://t.me'):
                            a = '@' + str(link.split('/')[3])
                            if a in exlist:
                                await message.reply(
                                    self.strings("ex").format(
                                    a
                                    )
                                )
                            else:
                                await message.reply(f'/заразить {a}')
                        else:
                            await message.reply(
                                self.strings("hueta")
                            )
                        break
            await asyncio.sleep(3.3)   
        if not count_st:
            await message.reply(
                self.strings("no_sargs")
            )
        elif not count_hf:
            await message.reply(
                self.strings("no_link")
            )
        elif len(list_args) >= 5:
            await message.reply(
                self.strings("tzar")
            )
    async def оcmd(self, message):
        """Заражает всех по реплаю.\nИспользуй ответ на сообщение с @id/@user/link"""
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        err = "1"
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return
        json = JSON.loads(reply.to_json())
        try:
            for i in range(len(reply.entities)):
                try:
                    link = json["entities"][i]["url"]
                    if link.startswith('tg'):
                        users = '@' + link.split('=')[1]
                        if users in exlist:
                            await message.reply(
                                    self.strings("ex").format(
                                    users
                                    )
                                )
                        else:
                            await message.reply(f'/заразить {users}')
                    elif link.startswith('https://t.me'):
                        a = '@' 
                        if a in exlist:
                            await message.reply(
                                    self.strings("ex").format(
                                    a
                                    )
                                )
                        else:
                            await message.reply(f'/заразить {a}')
                    else:
                        await message.reply(
                            self.strings("hueta")
                        )
                except Exception:
                    blayt = reply.raw_text[json["entities"][i]["offset"]:json["entities"][i]["offset"] + json["entities"][i]["length"]]
                    if blayt in exlist:
                        await message.reply(
                            self.strings("ex").format(
                                blayt
                                )
                            )
                    else:
                        await message.reply("/заразить " + blayt)
                await asyncio.sleep(3.3)
        
        except TypeError:
            err = "2"
            await message.edit(
                self.strings("hueta")
            )
        if err != "2":
            await message.delete()
    async def искcmd(self, message):
        """Добавляет исключения для команд .з и .о\nИспользуй: .иск {@user/@id/reply}"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        exlistGet = self.db.get("NumMod", "exUsers")
        exlist = exlistGet.copy()
        if not args:
            #if reply:
            #    rid = "@" + str(reply.sender_id)


            if len(exlist) < 1:
                await message.reply(
                    self.strings("empty_zar")
                )
                return
            exsms = ''.join(f'<b>{count}.</b> <code>{i}</code>\n' for count, i in enumerate(exlist, start=1))
            await utils.answer(message, exsms)
            return
        #if reply:
        if args == 'clear':
            exlist.clear()
            self.db.set("NumMod", "exUsers", exlist)
            await message.reply(
                self.strings("clrex")
            )
            return
        if len(args.split(' ')) > 1 or args[0] != '@':
            await message.reply(
                self.strings("too_much_args")
            )
            return
        if args in exlist:
            exlist.remove(args)
            self.db.set("NumMod", "exUsers", exlist)
            await message.edit(
                self.strings("exrm").format(
                    args
                )
            )
            return
        exlist.append(args)
        self.db.set("NumMod", "exUsers", exlist)
        await message.edit(
            self.strings("exadd").format(
                args
            )
        )
    async def зарcmd(self, message):
        """ Список ваших заражений.\n.зар {@id/user} {count} {args}\nДля удаления: .зар {@id/user}\nАргументы:\nк -- добавить букву k(тысяч) к числу.\nф -- поиск по ид'у/юзеру.\nр -- добавлению в список по реплаю. """
        args = utils.get_args_raw(message)
        infList = self.db.get("NumMod", "infList")
        timezone = "Europe/Kiev"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        k = ''
        with contextlib.suppress(Exception):
            args_list = args.split(' ')
        ###
        if not args:
            if not infList:
                await message.edit(
                    self.strings("empty_zar")
                )
                return
            sms = ''.join(
                f'<b>• <code>{key}</code>  <code>{value[0]}</code> [<i>{value[1]}</i>]</b>\n' for key, value in
                infList.items())
            await utils.answer(message, sms)
            return
        ##
        ###
        if 'р' in args.lower():
            reply = await message.get_reply_message()
            
            if not reply:
                return await message.reply(
                    self.strings("no_zar_reply")
                )
            ##

            trueZ = 'подверг заражению'
            trueZ2 = 'подвергла заражению' # да, я еблан)
            text = reply.text
            if trueZ not in reply.text and trueZ2 not in reply.text:
                await message.reply(
                    self.strings("wrong_zar_reply")
                )
            else:  # ☣
                try:
                    ept = ""
                    text = reply.text
                    x = text.index('☣') + 4
                    count = text[x:].split(' ', maxsplit=1)[0]
                    x = text.index('user?id=') + 8
                    user = '@' + text[x:].split('"', maxsplit=1)[0]
                    infList[user] = [str(count), vremya]
                    self.db.set("NumMod", "infList", infList)
                    await message.reply(
                        self.strings("r.save").format(
                            user, count, ept
                        )
                    )
                except ValueError:
                    await message.reply(
                        self.strings("nolink")
                    )
        elif args_list[0] == "clear84561":
            infList.clear()
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("clrzar")
            )

        elif 'ф' in args.lower():
            reply = await message.get_reply_message()

            if not reply:            
            
                if re.fullmatch(r"@\d{3,10}", args_list[0], flags=re.ASCII):
                    zhertva = args_list[0]

                if re.fullmatch(r"@\D\w{3,32}", args_list[0], flags=re.ASCII):
                    try:
                        get_id = await message.client.get_entity(args_list[0])
                        get_id = get_id.id
                        zhertva = "@" + str(get_id)
                    except:
                        return await message.reply(
                            self.strings("no_user").format(
                                args_list[0]
                            )
                        ) 

                if zhertva in infList:
                    user = infList[zhertva]
                    await message.reply(
                        self.strings("search").format(
                            zhertva, user[0], user[1]
                        )
                    )
                if zhertva not in infList:   
                    await message.reply(
                        self.strings("nf")
                    )  

            if reply: # <- костыль для фикса UnboundLocalError: local variable 'reply' ...
                rid = '@' + str(reply.sender_id)

                zhertva = "R#C*N("

                if re.fullmatch(r"@\d{3,10}", args_list[0], flags=re.ASCII):
                    zhertva = args_list[0]

                if re.fullmatch(r"@\D\w{3,32}", args_list[0], flags=re.ASCII):
                    try:
                        get_id = await message.client.get_entity(args_list[0])
                        get_id = get_id.id
                        zhertva = "@" + str(get_id)
                    except:
                        return await message.reply(
                            self.strings("no_user").format(
                                args_list
                            )
                        )                


                if zhertva in infList:
                    user = infList[zhertva]
                    await message.reply(
                        self.strings("search").format(
                            zhertva, user[0], user[1]
                        )
                    )                             
                elif rid in infList:
                    user = infList[rid]
                    await message.reply(
                        self.strings("search").format(
                            rid, user[0], user[1]
                        )
                    )              
                        
                elif rid not in infList:
                        await message.reply(
                            self.strings("nf")
                        )
        elif len(args_list) == 1 and args_list[0] in infList:
            infList.pop(args_list[0])
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("zar_rm").format(
                    args
                )
            )

        else:
            k = ''
            pas = 0
            try:
                user, count = str(args_list[0]), float(args_list[1])
            except Exception:
                try:
                    if "к" in args_list[1] or "k" in args_list[1]:
                        user = str(args_list[0])
                        args = str(args_list[1])
                        len_args = len(args_list[1])
                        count = args[:len_args-1]
                        count = float(count)
                        k += 'k'
                        pas = 1
                except: 
                    return await message.reply(
                        self.strings("wrong_cmd")
                    )                
            if re.fullmatch(r"@\D\w{3,32}", user, flags=re.ASCII):
                try:
                    get_id = await message.client.get_entity(user)
                    get_id = get_id.id
                    user = "@" + str(get_id)
                except:
                    pass              
            if 'к' in args.lower() and pas == 0 or 'k' in args.lower() and pas == 0:
                k += "k"     
            infList[user] = [str(count) + k, vremya]
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("r.save").format(
                            user, count, k
                )
            )
    
    async def довcmd(self, message):
        """ {args1} {args2 OR reply} \nВведи команду для просмотра аргументов."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        wnik = await self._client(GetFullUserRequest(message.sender_id))
        ent = wnik.users[0]
        a = self.config
        pref = self.get_prefix()
        dovs = ""
        if a["Доступ к лабе"]:
            dovs += "лабе, "
        if a["Доступ к заражениям"]:
            dovs += "заражениям, "
        if a["Доступ к прокачке"]:
            dovs += "прокачкам, "
        if a["Доступ к зарлисту"]:
            dovs += "зарлисту, "        
        if a["Доступ к жертвам"]:
            dovs += "жертвам, "
        if a["Доступ к болезням"]:
            dovs += "болезням, "
        if a["Доступ к вирусам"]:
            dovs += "установке вирусов, "
        if a["Доступ к хиллингу"]:
            dovs += "хиллингу, "
        len_dovs = len(dovs)
        dovs_accept = dovs[:len_dovs-2]

        dov_users = ', '.join(
            f'<code>@{i}</code>' for i in filter_and_users['users']
        )
        if not args:
            return await self.inline.form(
                self.strings("dov").format(
                    dov_users,
                    filter_and_users['filter'] or '❌ Не установлен.',
                    '✅ Запущен' if self.config["Вкл/выкл"] else '❎ Остановлен',
                    ent.first_name if len(ent.first_name) <= 12  else "ник",
                    dovs_accept if dovs_accept != "" else "всё ограничено 👌",
                    pref
                ),
                reply_markup={
                    "text": "Закрыть",
                    "callback": self.inline__close,

                },
                message=message,
                disable_security=False
            )
        args = args.split(' ', maxsplit=1)
        if len(args) == 1 and not reply and args[0] != 'пуск': # 
            return await utils.answer(message, '🤔 Не могу понять, что за хуета?..')
        
        elif args[0] == 'сет':
            try:
                user_id = args[1]
                if not user_id.isdigit():
                    return await message.reply(
                        self.strings("wrong_id")
                    )

            except Exception:
                user_id = str(reply.sender_id)
            
            if user_id in filter_and_users['users']:
                filter_and_users['users'].remove(user_id)
                return await message.reply(
                    self.strings("user_rm").format(
                        user_id
                    )
                )
            elif user_id not in filter_and_users['users']:
                filter_and_users['users'].append(user_id)
                return await message.reply(
                    self.strings("user_add").format(
                        user_id
                    )
                )

            return self.db.set("NumMod", "numfilter", filter_and_users)
        
        elif args[0] == 'ник':
            try:
                filter_and_users['filter'] = args[1].lower().strip()
                self.db.set("NumMod", "numfilter", filter_and_users)
                return await message.reply(
                    self.strings("nick_add").format(
                        args[1]
                    )
                )
            except Exception:
                return await message.reply(
                    self.strings("wrong_nick")
                )

        
        elif args[0] == 'пуск':
            if self.config["Вкл/выкл"]:
                self.config["Вкл/выкл"] = False
                return await message.reply(
                    self.strings("dov_stop")
                )

            else:
                self.config["Вкл/выкл"] = True
                return await message.reply(
                    self.strings("dov_start")
                )

        else:
            return await message.reply(
                self.strings("dov.wrong_args")
            )

    
    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        user_id = str(message.sender_id)
        nik = filter_and_users["filter"]
        text = message.raw_text.lower()
        if not nik or not self.config["Вкл/выкл"] or user_id not in filter_and_users['users']: 
            return

        if not text.startswith(nik): return
        
        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?(?P<link>@[0-9a-z_]+|(?:https?://)?t\.me/[0-9a-z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))",
                text
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['link'], send_mesа['id'] = '@' + send_mesа['id'] if send_mesа['id'] else send_mesа['link'], ''
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)
###### чеки
        if self.config["Доступ к прокачке"] == True:  
            if send_mes := re.search(r"(?P<ch>зараз[куаность]{,5} чек[нутьиай]{,4}\s|чек[айниуть]{,4} зараз[куаность]{,5}\s)(?P<lvl>[0-5]+)", text):
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
            elif send_mes := re.search(r"(?P<sb>сб чек[айниуть]{,4}\s|безопасно[сть]{,3} чек[айниуть]{,4}\s|служб[ау]{,2} чек[айниуть]{,4}\s|чек[айниуть]{,4} служб[ау]{,2}\s|чек[айниуть]{,4} безопасно[сть]{,3}\s|чек[айниуть]{,4} сб\s)(?P<lvl>[0-5]+)", text):
                send_mes = send_mes.groupdict()
                send_mes['sb'] = '+безопасность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
#### кач    алки
            elif send_mes := re.search(r"(?P<zar>зараз[уканость]{,5}\s)(?P<lvl>[0-5]+)", text):
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
            elif send_mes := re.search(r"(?P<sb>сб\s|безопасно[сть]{,3}\s|служб[ау]{,2}\s)(?P<lvl>[0-5]+)", text):
                send_mes = send_mes.groupdict()
                send_mes['sb'] = '++безопасность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            
        if self.config["Доступ к болезням"] == True:  
            if re.search(r"бол[езьни]{,5}\b", text):
                await message.reply('/мои болезни')
        
        if self.config["Доступ к жертвам"] == True:  
            if re.search(r"жертв[ыау]{,2}|еж[ау]{,2}", text):
                await message.reply('/мои жертвы')

        if self.config["Доступ к вирусам"] == True:  
            if re.search(r"-вирус[ыа]{,2}", text):
                await message.reply('-вирусы')
            if re.search(r"увед[ыаомления]{,8}", text):
                await message.reply('+вирусы')
        
        if self.config["Доступ к хиллингу"] == True:    
            if re.search(r"вак[цинау]{,3}|леч[ись]{,2}|хи[лльсяйинг]{,2}|лек[арство]{,2}", text):
                await message.respond('/купить вакцину')
            if re.search(r"цен[ау]{,2}|вч[ек]{,2}", text):
                await message.reply('<i>купить вакцину</i>')
        
        if self.config["Доступ к лабе"] == True:
            if re.search(r"" + nik + "%лаб[уа]{,2}|/лаб[уа]{,2}|#лаб[уа]{,2}", text):
                await message.reply('👇')
                await message.respond('/моя лаба')


#######################################################
        if self.config["Доступ к зарлисту"] == True:
            if re.search(r"(?P<zarlist>з\s)(?P<link>@[0-9a-z_]+|tg://openmessage\?user_id=[0-9]+)",
                text):
                if not text.startswith(f"{nik} з") and not text.startswith(nik + "з"):
                    return
                infList = self.db.get("NumMod", "infList")
                timezone = "Europe/Kiev"
                vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
                with contextlib.suppress(Exception):
                    text_list = text.split(' ', maxsplit=2)    
                if text_list[2] in infList:
                    user = infList[text_list[2]]
                    await message.reply(
                        self.strings("search").format(
                            text_list[2], user[0], user[1]
                        )
                    )
                if text_list[2] not in infList:
                    await message.reply(
                        self.strings("nf")
                    )
                else:
                    return
            if re.search(r"з", text):
                if text != f"{nik} з" and text != f"{nik}з":
                    return
                reply = await message.get_reply_message()
                infList = self.db.get("NumMod", "infList")
                timezone = "Europe/Kiev"
                vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
                try:
                    rid = '@' + str(reply.sender_id)
                except AttributeError: pass
                if not reply:
                    return
                if rid in infList:
                    user = infList[rid]
                    await message.reply(
                        self.strings("search").format(
                            rid, user[0], user[1]
                        )
                    )              
                        
                elif rid not in infList:
                        await message.reply(
                            self.strings("nf")
                        )  
                else:
                    return
#######################################################

###     
    async def гcmd(self, message):
        " [arg] [arg] [arg]....\nВыполняет команду /ид по реплаю\n Аргументом являются числа и первые символы строки. "
        reply = await message.get_reply_message()
        
        count_st = 0
        count_hf = 0
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return

        args = utils.get_args_raw(message)
        list_args=[]
        if not args:
            await message.reply(
                self.strings("not_args")
            )
            return
        a = reply.text
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    for x in range(int(ot_do[0]),int(ot_do[1])+1):
                        list_args.append(str(x))
                except:
                    await message.reply(
                        self.strings("ot_do")
                    )
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
                            await message.reply(
                                self.strings("hueta")
                            )
                            break
            await asyncio.sleep(3)
        if not count_st:
            await message.reply(
                self.strings("no_sargs")
            )
        elif not count_hf:
            await message.reply(
                self.strings("nolink")
            )
        elif len(list_args) >= 5:
            await message.respond(
                self.strings("tids")
            )
            await asyncio.sleep(3.3)

    async def иcmd(self, message):
        """Чекает все айди по реплаю.\nИспользуй ответ на сообщение с @id/@user/link"""
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return
  
        for i in range(len(reply.entities)):
            try:
                json = JSON.loads(reply.to_json())
                link = json["entities"][i]["url"]
                if link.startswith('tg'):
                    users = '@' + link.split('=')[1]
                    if users in exlist:
                        await message.reply(f'/id <code>{users}</code>')
                    else:
                        await message.reply(f'/id <code>{users}</code>')
                elif link.startswith('https://t.me'):
                    a = '@' 
                    if a in exlist:
                        await message.reply(f'/id <code>{a}</code>')
                    else:
                        await message.reply(f'/id <code>{a}</code>')
                else:
                    await message.reply('🤔 не могу найти ебанные иды')
            except Exception:
                await message.reply("/id " + '<code>' + reply.raw_text[
                                              json["entities"][i]["offset"]:json["entities"][i]["offset"] +
                                                                            json["entities"][i]["length"]] + '</code>')
            await asyncio.sleep(3.3)
        await message.delete()
    
    async def бcmd(self, message):
        """Используй ответом на биотопы/жертвы и т.п"""
        bt, bch, bk, btz, bchz, ezha, bol = "🔬 ТОП ЛАБОРАТОРИЙ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:","🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:","🔬 ТОП КОРПОРАЦИЙ ПО ЗАРАЖЕНИЯМ:","🔬 ТОП БОЛЕЗНЕЙ:","🔬 ТОП БОЛЕЗНЕЙ БЕСЕДЫ:","🦠 Список больных вашим патогеном:","🤒 Список ваших болезней:"
        reply = await message.get_reply_message()
        if not reply:
            await message.edit(
                self.strings("not_reply")
               )
            return
        a = reply.text
        sms = ''
        if "🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ" in a:
            sms += "🥰 топ вкусняшек чата:\n"
            
        if "🔬 ТОП ЛАБОРАТОРИЙ ПО" in a:
            sms += "🔬 ТОП ЛАБОРАТОРИЙ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:\n"

        if bt not in a and bch not in a and bk not in a and btz not in a and bchz not in a and ezha not in a and bol not in a:
            await message.respond(
                self.strings("hueta")
            )
            return 
        b = reply.raw_text.splitlines() 
        b.pop(0)
        hh = []
        for i in b:
            try:
                hh.append(i.split('|')[1])
            except: pass
        json = JSON.loads(reply.to_json())
        
        count = 1
        for i in range(0, len(reply.entities) ):
            try:
                exp = hh[i]
            except:
                exp = i
            link = json["entities"][i]["url"]
            try:
                if link.startswith('tg'):
                    bla = []
                    for i in link.split('='):
                        bla.append(i)
                    b = await message.client.get_entity(int(bla[1]))
                    
                    b_first_name = utils.validate_html(b.first_name)
                    
                    sms += f'{str(count)}. <b>{b_first_name}</b> - <code>@{b.id}</code> | <u>{exp}</u>\n'
                
                elif link.startswith('https://t.me'):
                    a = '@' + str(link.split('/')[3])
                    sms += f'{str(count)}. <code>{a}</code> | <u>{result}</u>\n'
                else:
                    sms += f'{str(count)}. что за хуета?\n'
            except:
                if link.startswith('https://t.me'):
                    a ='@' + str(link.split('/')[3])
                    sms += f'{str(count)}. <code>{a}</code> | <u>{exp}</u> \n'
                elif link.startswith('tg'):
                    bla = []
                    for i in link.split('='):
                        bla.append(i)
                    sms += f'{str(count)}. <b>??????</b> - <code>@{bla[1]}</code> | <u>{exp}</u> \n'
            count += 1

        await self.inline.form(
            sms,
            reply_markup={
                            "text": f"🔻 Close",
                            "callback": self.inline__close,
            },
            message=message,
            disable_security=False
        )   
### помощь
    async def biohelpcmd(self, message: Message):
        """Выдает помощь по модулю"""
        pref = self.get_prefix()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message(
        )
        if not args:
            await self.inline.form(
                self.strings("guide").format(
                        pref
                ),
                reply_markup={
                                "text": "Закрыть",
                                "callback": self.inline__close,
                },
            message=message,
            disable_security=False
            )
#######################   
        if 'дов' in args:
            nnik = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
            nik = nnik['filter'] or 'ник' 
            await self.inline.form(
                self.strings("guidedov").format(
                    nik, pref
                ),
                reply_markup={
                    "text": "Закрыть",
                    "callback": self.inline__close,

                },
                message=message,
                disable_security=False
            )   

    async def inline__close(self, call) -> None:
        await call.delete()

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Доступ к лабе",
                False,
                "Доступ к лабе через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к заражениям",
                True,
                "Доступ к команде заражения через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к прокачке",
                False,
                "Доступ к прокачке навыков через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к зарлисту",
                False,
                "Доступ к поиску жертв в зарлисте через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к жертвам",
                True,
                "Доступ к жертвам через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к болезням",
                True,
                "Доступ к болезням через доверку",
                validator=loader.validators.Boolean(),
            ),

            loader.ConfigValue(
                "Доступ к вирусам",
                False,
                "Доступ к установке вирусов через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к хиллингу",
                True,
                "Доступ к покупке вакцины",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Вкл/выкл",
                False,
                "Включение и отключение доверки"
                "\n❗️ Не влияет на отключение доверки в других Num'модулях.",
                validator=loader.validators.Boolean(),
            )
        )