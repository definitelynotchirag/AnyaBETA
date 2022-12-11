 # """
# MIT License 

# Copyright (c) 2021 TheHamkerCat

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# """

"""
import os
from asyncio import gather, get_running_loop
from base64 import b64decode
from io import BytesIO
from random import randint
import urllib
import urllib.parse
from gpytranslate import SyncTranslator
trans = SyncTranslator()

import aiofiles
import requests
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message

# from nezuko import MESSAGE_DUMP_CHAT, SUDOERS, app, eor
# from nezuko.core.decorators.errors import capture_err
# from nezuko.utils.functions import get_file_id_from_message
# from nezuko.utils.http import get

from NekoRobot import JOIN_LOGGER as MESSAGE_DUMP_CHAT
from NekoRobot import DRAGONS as SUDOERS
from NekoRobot import pgram as app
from telegram import ParseMode, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from NekoRobot import eor 
from NekoRobot.utils.errors import capture_err
from NekoRobot.utils.functions import get_file_id_from_message
from NekoRobot.utils.http import get

from inspect import getfullargspec

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


async def get_soup(url: str, headers):
    html = await get(url, headers=headers)
    return BeautifulSoup(html, "html.parser")


@app.on_message(filters.command(["reverse", "pp", "grs"]))
@capture_err
async def reverse_image_search(client, message: Message):
    if not message.reply_to_message:
        return await eor(
            message, text="Reply to a message to reverse search it."
        )
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        return await eor(
            message,
            text="Reply to an image/document/sticker/animation to reverse search it.",
        )
    m = await eor(message, text="Searching...")
    mesg = "Possible Results- \n"
    file_id = get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Can't reverse that")
    image = await client.download_media(file_id, f"{randint(1000, 10000)}.jpg")
    async with aiofiles.open(image, "rb") as f:
        if image:
            search_url = "https://yandex.com/images/"
            multipart = {
                "encoded_image": (image, await f.read()),
                "image_content": "",
            }

            def post_non_blocking():
                return requests.post(
                    search_url, files=multipart, allow_redirects=False
                )

            loop = get_running_loop()
            response = await loop.run_in_executor(None, post_non_blocking)
            location = response.headers.get("Location")
            print(location)
            os.remove(image)
        else:
            return await m.edit("Something wrong happened.")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
    }

    buttons = [[InlineKeyboardButton("View Similar Images", url=location)]]


    try:

        opener = urllib.request.build_opener()
        source = opener.open(location).read()
        # soup = await get_soup(location, headers=headers)
        soup = BeautifulSoup(source, "html.parser")
        
        # for similar_image in soup.findAll("input", {"class": "gLFyf"}):
        #     url = urllib.parse.quote_plus(
        #         similar_image.get("value")
        #     )
        div = soup.find_all("a", {"class": "Button2 Button2_size_l Button2_type_link Button2_view_default Button2_width_auto Tags-Item"})
        # # div = soup.find_all("div", {"class": "r5a77d"})
        # # text = div.find("a").text
        # text = f"**Result**: [{url}]({location}) \nBest Guess:{url}"
        if div == None:
            await m.edit("Nothing Found")

       
        for word in div:
            text = word.find().text
            # source = trans.detect(text)
            # dest = "en"
            # translation = trans(text, sourcelang=source, targetlang=dest)
            mesg += f"`{text}` \n"


        source = trans.detect(mesg)
        dest = "en"
        translation = trans(mesg, sourcelang=source, targetlang=dest)
        eww = translation.text
        # print(mesg)


    except Exception:
        await m.edit("Error")
        # for best_guess in soup.findAll("div", attrs={"class": "UAiK1e"}):
        #     xd = best_guess.get_text()


        # return await m.edit(
        #     f"**Result**: [{xd}]({location}) \nBest Guess: {xd}",
        #     disable_web_page_preview=True,
        #     parse_mode="Markdown",
        #     # reply_markup=InlineKeyboardMarkup(buttons)
        #     # parse_mode=ParseMode.MARKDOWN_V2
        # )

    # Pass if no images detected
    try:
        url = "https://google.com" + soup.find_all(
            "a", {"class": "ekf0x hSQtef"}
        )[0].get("href")

        soup = await get_soup(url, headers=headers)

        media = []
        for img in soup.find_all("img"):
            if len(media) == 2:
                break

            if img.get("src"):
                img = img.get("src")
                if "image/gif" in img:
                    continue

                img = BytesIO(b64decode(img))
                img.name = "img.png"
                media.append(img)
            elif img.get("data-src"):
                img = img.get("data-src")
                media.append(img)

        # Cache images, so we can use file_ids
        tasks = [client.send_photo(MESSAGE_DUMP_CHAT, img) for img in media]
        messages = await gather(*tasks)

        await message.reply_media_group(
            [
                InputMediaPhoto(
                    i.photo.file_id,
                    caption=text,
                )
                for i in messages
            ]
        )
    except Exception:
        pass

    await m.edit(
        eww,
        disable_web_page_preview=True,
        parse_mode="Markdown",
        # reply_markup=InlineKeyboardMarkup(buttons)
        # parse_mode=ParseMode.MARKDOWN_V2
    )

"""

# __mod_name__ = "Reverse"
# __help__ = """
# *Reverse*
#  ❍ `/pp` : Please reply to a sticker, or an image to search it!
#  ❍ `/reverse` : Please reply to a sticker, or an image to search it!
# """


