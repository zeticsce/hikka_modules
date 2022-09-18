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
# Name: filter
# Description: Filters module
# Author: GeekTG
# Commands:
# .filter | .stop | .stopall | .filters
# ---------------------------------------------------------------------------------

# -*- coding: utf-8 -*-

# Module author: @ftgmodulesbyfl1yd

from .. import loader, utils
import time

@loader.tds
class FiltersSBMod(loader.Module):
    """Filters module"""

    strings = {"name": "FiltersSB"}

    async def client_ready(self, client, db):
        self.db = db

    async def fltcmd(self, message):
        """Adds a filter into the list."""
        filters = self.db.get("AutoFilters", "Autofilters", {})
        key = utils.get_args_raw(message).lower()
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)

        if not key and not reply:
            return await message.edit("<b>No args or reply.</b>")

        if chatid not in filters:
            filters.setdefault(chatid, {})

        if key in filters[chatid]:
            return await message.edit("<b>Such a filter already exists.</b>")

        if reply:
            if key:
                msgid = await self.db.store_asset(reply)
            else:
                return await message.edit(
                    "<b>You need arguments to save the filter!</b>"
                )
        else:
            try:
                msgid = (
                    await message.client.send_message(
                        f"friendly-{(await message.client.get_me()).id}-assets",
                        key.split("/")[1],
                    )
                ).id
                key = key.split("/")[0]
            except IndexError:
                return await message.edit(
                    "<b>Need a second argument (through / ) or a reply.</b>"
                )

        filters[chatid].setdefault(key, msgid)
        self.db.set("AutoFilters", "Autofilters", filters)
        await message.edit(f'<b>Filter "{key}" saved!</b>')

    async def fltstopcmd(self, message):
        """Removes a filter from the list."""
        filters = self.db.get("AutoFilters", "Autofilters", {})
        args = utils.get_args_raw(message)
        chatid = str(message.chat_id)

        if chatid not in filters:
            return await message.edit("<b>There are no filters in this chat.</b>")

        if not args:
            return await message.edit("<b>No args.</b>")

        if args:
            try:
                filters[chatid].pop(args)
                self.db.set("AutoFilters", "Autofilters", filters)
                await message.edit(f'<b>Filter "{args}" removed from chat list!</b>')
            except KeyError:
                return await message.edit(f'<b>No "{args}" filter.</b>')
        else:
            return await message.edit("<b>No args.</b>")

    async def stopallfltcmd(self, message):
        """Clears out the filter list."""
        filters = self.db.get("AutoFilters", "Autofilters", {})
        chatid = str(message.chat_id)

        if chatid not in filters:
            return await message.edit("<b>There are no filters in this chat.</b>")

        filters.pop(chatid)
        self.db.set("AutoFilters", "Autofilters", filters)
        await message.edit("<b>All filters have been removed from the chat list!</b>")

    async def fltscmd(self, message):
        """Shows saved filters."""
        filters = self.db.get("AutoFilters", "Autofilters", {})
        chatid = str(message.chat_id)

        if chatid not in filters:
            return await message.edit("<b>There are no filters in this chat.</b>")

        msg = ""
        for _ in filters[chatid]:
            msg += f"<b>• {_}</b>\n"
        await message.edit(
            f"<b>List of filters in this chat: {len(filters[chatid])}\n\n{msg}</b>"
        )

    async def watcher(self, message):

        filters = self.db.get("AutoFilters", "Autofilters", {})
        chatid = str(message.chat_id)
        m = message.text.lower()
        if chatid not in filters:
            return
        for _ in filters[chatid]:
            msg = await self.db.fetch_asset(filters[chatid][_])
            def_pref = self.db.get("friendly-telegram.main", "command_prefix")
            pref = "." if not def_pref else def_pref[0]
            if len(_.split()) == 1:
                if _ in m.split():
                    await self.exec_comm(msg, message, pref)
            else:
                if _ in m:
                    await message.reply("/купить вакцину")
                    time.sleep(4)
                    await self.exec_comm(msg, message, pref)

    async def exec_comm(self, msg, message, pref):
        try:
            if msg.text[0] == pref:
                smsg = msg.text.split()
                return await self.allmodules.commands[smsg[0][1:]](
                    await message.reply(
                        smsg[0] + " ".join(_ for _ in smsg if len(smsg) > 1)
                    )
                )
            else:
                pass
        except:
            pass
        await message.reply(msg)