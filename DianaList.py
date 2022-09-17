__version__ = (2, 0, 0)

#			███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
#			╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
#			░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
#			██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
#			███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
#			╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
#  				                 © Copyright 2022
#  				              https://t.me/zeticsce
#  				
#  				    🔒         Licensed under the GNU AGPLv3
#  				    🌐 https://www.gnu.org/licenses/agpl-3.0.html
from .. import loader, utils  # noqa
from datetime import datetime, date, time
import pytz
import contextlib
# meta developer: @zeticsce

@loader.tds
class DianaListMod(loader.Module):
    """zxczarlist"""
    strings = {
        "name": "zxczarlist",
        "r.save":   
            "🦠 Жертва <b><code>{}</code></b> сохранена.\n"
            "<b>☣️ +{}{}</b> био-опыта.",
        "search":
            "<emoji document_id=5212932275376759608>✅</emoji> Жертва <code>{}</code> приносит:\n"
            "<b>☣️ +{} био-опыта.</b>\n"
            "📆 Дата: <i>{}</i>",
        "nf": "❎ Жертва не найдена."
    }
    
    async def client_ready(self, client, db):
        self.db = db
        if not self.db.get("DianaNumMod", "DianainfList", False):
            self.db.set("DianaNumMod", "DianainfList", {})

    async def зрcmd(self, message):
        """ Список ваших заражений.\n.зр {@id/user/reply} {count} {args}\nДля удаления: .зар {@id/user}\nАргументы:\nк -- добавить букву k(тысяч) к числу.\nф -- поиск по ид'у/юзеру/реплаю.\nр -- добавлению в список по реплаю. """
        args = utils.get_args_raw(message)
        infList = self.db.get("DianaNumMod", "DianainfList")
        timezone = "Asia/Almaty"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        with contextlib.suppress(Exception):
            args_list = args.split(' ')
        ###
        if not args:
            if not infList:
                await utils.answer(message, "❌ Список заражений пуст.")
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
                return await utils.answer(message, '❌ Нет реплая на сообщение ириса о заражении.')
            ##

            trueZ = 'подверг заражению'
            trueZ2 = 'подвергла заражению' # да, я еблан)
            text = reply.text
            if trueZ not in reply.text and trueZ2 not in reply.text:
                await message.reply('❌ Реплай <b>не</b> на сообщение ириса о заражении "<b>...подверг заражению...</b>"')
            else:  # ☣
                try:
                    ept = ""
                    text = reply.text
                    x = text.index('☣') + 4
                    count = text[x:].split(' ', maxsplit=1)[0]
                    x = text.index('user?id=') + 8
                    user = '@' + text[x:].split('"', maxsplit=1)[0]
                    infList[user] = [str(count), vremya]
                    self.db.set("DianaNumMod", "DianainfList", infList)
                    await message.reply(
                        self.strings("r.save").format(
                            user, count, ept
                        )
                    )
                except ValueError:
                    await message.reply('😣 Нет ссылки на жертву.')
        elif args_list[0] == "clear":
            infList.clear()
            self.db.set("DianaNumMod", "DianainfList", infList)
            await message.reply(
                "✅ Зарлист <b>очищен</b>."
            )
        elif 'ф' in args.lower():
            reply = await message.get_reply_message()
            if not reply:            
                if args_list[0] in infList:
                    user = infList[args_list[0]]
                    await message.reply(
                        self.strings("search").format(
                            args_list[0], user[0], user[1]
                        )
                    )
                if args_list[0] not in infList:
                    if  '@' not in args:
                        await message.reply(
                            "<emoji document_id=5379667175004969388>🤔</emoji> а кого искать?.."
                        )
                    else:    
                        await message.reply(
                            self.strings("nf")
                        )      
            if reply:
                rid = '@' + str(reply.sender_id)  
                if args_list[0] in infList:
                    user = infList[args_list[0]]
                    await message.reply(
                        self.strings("search").format(
                            args_list[0], user[0], user[1]
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
                f"❎ Жертва <b><code>{args}</code></b> удалена из списка."
            )

        else:
            try:
                user, count = str(args_list[0]), float(args_list[1])
            except Exception:
                await message.reply( 
                    "❌ Команда введена некорректно."
                    )
                return
            k = ''
            if 'к' in args.lower():
                k += 'k'
            infList[user] = [str(count) + k, vremya]
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("r.save").format(
                            user, count, k
                )
            )