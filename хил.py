from .. import loader, utils
import asyncio, pytz, re, telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time

class HENumMod(loader.Module):
	"лечит долбоёбов."
	strings={"name": "хил"}
	
	async def client_ready(self, client, db):
		self.db = db
		if not self.db.get("HENumMod", "exUsers", False):
			self.db.set("HENumMod", "exUsers", [])
		if not self.db.get("HENumMod", "infList", False):
			self.db.set("HENumMod", "infList", {})
	async def hillcmd(self, message):
		""" .Введи .hill для инструкции"""
		args = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		filter_and_users = self.db.get("HENumMod", "hill", {'users': [], 'filter': None, 'status': False})
		if not args:
			return await utils.answer(message, f"-sU --- добавить|удалить юзеров(не больше 20), на которых будет триггериться фильтр(ид|реплай).\n[{', '.join(list('<code>' + i + '</code>' for i in filter_and_users['users']))}]\n-sF --- установить фильтр. Допустим один.\n<code>{filter_and_users['filter'] if filter_and_users['filter'] else '❌Не установлен.'}</code>\n-t --- запустить|остановить.\n<b>{'✅Запущен' if filter_and_users['status'] else '❌Остановлен'}.</b>\n\n"
				f"Для настройки модуля введи команды ниже:\n"
				f"<code>.hill -sF хи</code>\n\n"
				f"<code>.hill -sU</code> (ответом на это сообщение)\n\n"
				f"<code>.hill -t</code>"
			)
		args = args.split(' ', maxsplit=1)
		if len(args) == 1 and not reply and args[0] != '-t':
			return await utils.answer(message, '❌ Нет 2 аргумента и реплая.')
		elif args[0] == '-sU':
			try:
				user_id = args[1]
				if not user_id.isdigit():
					return await utils.answer(message, 'Это не ид.')
			except:
				user_id = str(reply.sender_id)
			if user_id in filter_and_users['users']:
				filter_and_users['users'].remove(user_id)
				await utils.answer(message, f"✅ Ид <code>{user_id}</code> удалён.")
			elif len(filter_and_users['users']) <= 20:
				filter_and_users['users'].append(user_id)
				await utils.answer(message, f"✅ Ид <code>{user_id}</code> добавлен.")
			else:
				return await utils.answer(message, '❌ Превышен лимит в 5 юзеров.')
			return self.db.set("HENumMod", "hill", filter_and_users)
		elif args[0] == '-sF':
			try:
				filter_and_users['filter'] = args[1].lower().strip()
				self.db.set("HENumMod", "hill", filter_and_users)
				return await utils.answer(message, f"✅ Фильтр ~~~ <code>{args[1]}</code> ~~~ успешно установлен!")
			except:
				return await utils.answer(message, "Где 2 аргумент❓")
		elif args[0] == '-t':
			if filter_and_users['status']:
				filter_and_users['status'] = False
				self.db.set("HENumMod", "hill", filter_and_users)
				return await utils.answer(message, "❌ Фильтр остановлен.")
			else:
				filter_and_users['status'] = True
				self.db.set("HENumMod", "hill", filter_and_users)
				return await utils.answer(message, "✅ Фильтр запущен.")
		else:
			return await utils.answer(message, "❌ Неизвестный аргумент.")

	async def watcher(self, message):
		if not isinstance(message, telethon.tl.types.Message): return
		filter_and_users = self.db.get("HENumMod", "hill", {'users': [], 'filter': None, 'status': False})
		user_id = str(message.sender_id)
		if not filter_and_users['filter'] or not filter_and_users['status'] or user_id not in filter_and_users['users'] or message.is_private: return
		text = message.raw_text.lower()
		if not text.startswith(filter_and_users['filter']): return
		
		send_mes = re.search(r"хи[лльсяйинг]{,5}", text)
		if send_mes: 
			await message.respond('/купить вакцину')
			await message.delete()
