# -*- coding: utf-8 -*-

# Module author: @DneZyeK

import itertools
import logging
import sys
import traceback
import types

import telethon
from meval import meval

from .. import loader, utils

loggerNxec = logging.getLogger(__name__)
logger = logging.getLogger("friendly-telegram.modules.notes")


@loader.tds
class NotexecAndNotesMod(loader.Module):
    """Stores global notes (aka snips)"""

    strings = {
        "name": "NotesKeK",
        
        
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

    async def notexeccmd(self, message):
        """Gets the note specified"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("what_note", message))
            return

        asset_id = self._db.get("friendly-telegram.modules.notes", "notes", {}).get(
            args[0], None
        )
        loggerNxec.debug(asset_id)
        if asset_id is not None:
            asset = await self._db.fetch_asset(asset_id)
        else:
            asset_id = self._db.get("friendly-telegram.modules.notes", "notes", {}).get(
                args[0].lower(), None
            )
            asset = (
                await self._db.fetch_asset(asset_id) if asset_id is not None else None
            )
        if asset is None:
            await utils.answer(message, self.strings("no_note", message))
            return

        cmd = await self._db.fetch_asset(asset_id)

        try:
            await meval(cmd.raw_text, globals(), **await self.getattrs(message))
        except Exception:
            exc = sys.exc_info()
            exc = "".join(
                traceback.format_exception(
                    exc[0], exc[1], exc[2].tb_next.tb_next.tb_next
                )
            )
            await utils.answer(
                message,
                self.strings("execute_fail", message).format(utils.escape_html(exc)),
            )
            return

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._db = db

    async def getattrs(self, message):
        return {
            "message": message,
            "client": self.client,
            "self": self,
            "db": self.db,
            "reply": await message.get_reply_message(),
            "event": message,
            "chat": message.to_id,
            **self.get_types(),
            **self.get_functions(),
        }

    def get_types(self):
        return self.get_sub(telethon.tl.types)

    def get_functions(self):
        return self.get_sub(telethon.tl.functions)

    def get_sub(self, it, _depth=1):
        """Get all callable capitalised objects in an object recursively, ignoring _*"""
        return {
            **dict(
                filter(
                    lambda x: x[0][0] != "_"
                    and x[0][0].upper() == x[0][0]
                    and callable(x[1]),
                    it.__dict__.items(),
                )
            ),
            **dict(
                itertools.chain.from_iterable(
                    [
                        self.get_sub(y[1], _depth + 1).items()
                        for y in filter(
                            lambda x: x[0][0] != "_"
                            and isinstance(x[1], types.ModuleType)
                            and x[1] != it
                            and x[1].__package__.rsplit(".", _depth)[0]
                            == "telethon.tl",
                            it.__dict__.items(),
                        )
                    ]
                )
            ),
        }

    async def notecmd(self, message):
        """Gets the note specified"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("what_note", message))
            return
        asset_id = self._db.get("friendly-telegram.modules.notes", "notes", {}).get(args[0], None)
        logger.debug(asset_id)
        if asset_id is not None:
            asset = await self._db.fetch_asset(asset_id)
        else:
            asset = None
        if asset is None:
            self.del_note(args[0])
            await utils.answer(message, self.strings("no_note", message))
            return
        await message.delete()
        await message.client.send_message(message.to_id, await self._db.fetch_asset(asset_id), reply_to=await message.get_reply_message())

    async def delallnotescmd(self, message):
        """Deletes all the saved notes"""
        if not self._db.get("friendly-telegram.modules.notes", "notes", {}):
            await utils.answer(message, self.strings("delnotes_none", message))
            return
        self._db.get("friendly-telegram.modules.notes", "notes", {}).clear()
        await utils.answer(message, self.strings("delnotes_done", message))

    async def savecmd(self, message):
        """Save a new note. Must be used in reply with one parameter (note name)"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("what_name", message))
            return
        if not message.is_reply:
            if len(args) < 2:
                await utils.answer(message, self.strings("save_what", message))
                return
            else:
                message.entities = None
                message.message = args[1]
                target = message
                logger.debug(target.message)
        else:
            target = await message.get_reply_message()
        asset_id = await self._db.store_asset(target)
        self._db.set("friendly-telegram.modules.notes", "notes", {**self._db.get("friendly-telegram.modules.notes", "notes", {}), args[0]: asset_id})
        await utils.answer(message, str(self.strings("saved", message)).format(args[0]))

    async def delnotecmd(self, message):
        """Deletes a note, specified by note name"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("delnote_args", message))
        self.del_note(args[0])
        await utils.answer(message, self.strings("delnote_done", message))

    def del_note(self, note):
        old = self._db.get("friendly-telegram.modules.notes", "notes", {})
        try:
            del old[note]
        except KeyError:
            pass
        else:
            self._db.set("friendly-telegram.modules.notes", "notes", old)

    async def notescmd(self, message):
        """List the saved notes"""
        if not self._db.get("friendly-telegram.modules.notes", "notes", {}):
            await utils.answer(message, self.strings("notes_none", message))
            return
        await utils.answer(message, self.strings("notes_header", message)
                           + "\n".join(self.strings("notes_item", message).format(key)
                           for key in self._db.get("friendly-telegram.modules.notes", "notes", {})))

    async def client_ready(self, client, db):
        self._db = db