__version__ = (1, 0, 0)

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

# meta developer: @zeticsce
from .. import loader, utils
import asyncio
import telethon
@loader.tds
class SBebMod(loader.Module):
    """
Покупает вакцину и бьет по сб
    """
    strings = {
        "name": "sbeb"

    }
    
    async def зоcmd(self, message):
        """
Используй: .зо {кол-во патов} [реплай]
        """
        try:
            reply = await message.get_reply_message()
            args = utils.get_args_raw(message)
            text = reply.text
            txt = text.splitlines()
            org = "Организатор заражения:"
        except:
            pass
        pat = ""
        if not reply:
            return await message.edit("где реплай на сб, дубина??")
        if args:
            try:
                pat = int(args)
            except:
                return await message.edit("что за хуйню ты ввел в аргументы? вводи число от 1 до 10") 
            pat = str(f"{pat} ") 
            if pat > 10 or pat == 0:
                return await message.reply("ты ввёл хуйню!")
        await message.reply("/купить вакцину")
        for i in txt:
            if i.lower().startswith(str(org.lower())):
                b = i.find('href="') + 6
                c = i.find('">')
                link = i[b:c]
                
                if link.startswith('tg'):
                    user = '@' + link.split('=')[1]
                    await asyncio.sleep(4)
                    await message.reply(
                        f"/заразить {pat}{user}"
                    )
                elif link.startswith('https://t.me'):
                    a = '@' + str(link.split('/')[3])
                    await asyncio.sleep(4)
                    await message.reply(
                        f"/заразить {pat}{a}"
                    )
                else: 
                    await message.reply("что за хуете")
