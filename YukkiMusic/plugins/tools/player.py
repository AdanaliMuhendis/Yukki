#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from YukkiMusic import app
from YukkiMusic.misc import db
from YukkiMusic.utils.decorators import AdminRightsCheck


@app.on_message(
    filters.command(["cplayer", "playing", "cplaying", "player"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    check = db.get(chat_id)
    reply_markup, thumbs, caption = (
        next(
            (
                item["mystic"].reply_markup
                for item in check
                if isinstance(item, dict)
                and "mystic" in item
                and hasattr(item["mystic"], "reply_markup")
            ),
            None,
        ),
        (
            next(
                (
                    item["mystic"].photo.thumbs
                    for item in check
                    if isinstance(item, dict)
                    and "mystic" in item
                    and hasattr(item["mystic"].photo, "thumbs")
                ),
                None,
            )
        )[0].file_id,
        next(
            (
                item["mystic"].caption
                for item in check
                if isinstance(item, dict)
                and "mystic" in item
                and hasattr(item["mystic"], "caption")
            ),
            None,
        ),
    )

    await message.reply_photo(photo=thumbs, caption=caption, reply_markup=reply_markup)
