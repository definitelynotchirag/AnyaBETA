import asyncio

from pyrogram import filters

# from NekoRobot import DRAGONS, pbot as app

import NekoRobot.modules.mongo.dalc_mongo as sql
from NekoRobot.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from NekoRobot import pgram as app
from telegram.ext import CallbackContext, Filters, MessageHandler
from telegram import MessageEntity, Update
from NekoRobot.ex_plugins.dbfunctions import(
    alpha_to_int,
    get_karma,
    # get_karmas,
    int_to_alpha,
    update_karma,
)

from NekoRobot.pyro.errors import capture_err
from NekoRobot.utils.filter_groups import karma_negative_group, karma_positive_group

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$"

@app.on_message(
  filters.text
  & filters.group
  & filters.incoming
  & filters.reply
  & filters.regex(regex_upvote)
  & ~filters.via_bot
  & ~filters.bot,
  group=karma_positive_group,
)
async def upvote(_,message):
#   chat_id = message.chat.id
#   is_karma = sql.is_karma(chat_id)
#   if not is_karma:
#         return
  if not message.reply_to_message.from_user:
        return
  if not message.from_user:
        return
  if message.reply_to_message.from_user.id == message.from_user.id:
        return
  user_id = message.reply_to_message.from_user.id
  user_mention = message.reply_to_message.from_user.mention
  current_karma = await get_karma(await int_to_alpha(user_id)
    )
  if current_karma:
        current_karma = current_karma['karma']
        karma = current_karma + 100
  else:
        karma = 100
  new_karma = {"karma": karma}
  await update_karma(await int_to_alpha(user_id), new_karma
    )
  await message.reply_text(
        f"Waku Waku! Anya added 100 dalcs to {user_mention}'s Wallet\nCurrent Dalcs: {karma}Đ"
    )

@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,  
)

async def downvote(_, message):
    # chat_id = message.chat.id
    # is_karma = sql.is_karma(chat_id)
    # if not is_karma:
    #     return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 100
    else:
        karma = 100
    new_karma = {"karma": karma}
    await update_karma(await int_to_alpha(user_id), new_karma)
    await message.reply_text(
        f"Anya is Sad :( took 100 dalcs from {user_mention}'s Wallet\nCurrent Dalcs: {karma}Đ"
    )

@app.on_message(filters.command("dalcstat") & filters.group)
async def karma(_, message):
    # chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Matte! Anya will ask chichi for wallets of this chat...")
        # karma = await get_karmas(chat_id)
        # if not karma:
        #     await m.edit("Anya is Sad. No Dalcs in DB for this chat.")
        #     return
        msg = f"Dalc list of {message.chat.title}:- \n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True)
            )
        if not karma_dicc:
            await m.edit("Anya is Sad. No Dalcs in DB for this chat.")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await app.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            msg += f"{karma_count}  {(first_name[0:12] + '...') if len(first_name) > 12 else first_name}  {('@' + username) if username else user_idd}\n"
            limit += 1
        await m.edit(msg)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(await int_to_alpha(user_id))
        karma = karma["karma"] if karma else 0
        await message.reply_text(f"Total Dalcs: {karma} Đ")

# @app.on_message(filters.command("dalcstat") & filters.group)
# async def mywallet(_, message):
#     chat_id = message.chat.id
#     user_id = message.reply_to_message.from_user.id
#     karma = await get_karma(chat_id, await int_to_alpha(user_id))
#     karma = karma["karma"] if karma else 0
#     await message.reply_text(f"Total Dalcs: {karma}Đ")

# KARMA_REGEX_HANDLER = DisableAbleMessageHandler(
#       filters.text
#     & filters.group
#     & filters.incoming
#     & filters.reply
#     & filters.regex(regex_downvote)
#     & ~filters.via_bot
#     & ~filters.bot,
#     group=karma_negative_group
# )

 # ❍ Reply to any meassage with (`+, +1, thx, thanx, thanks, pro, cool, good,pro, pero, op, nice, noice, best, uwu, owo, right, correct, peru, piro`, 👍) to increse karma of user.
 # ❍ Reply to any meassage with (`-, -1, 👎, noob, baka, idiot, chutiya, nub, noob, wrong, incorrect, chaprii, chapri, weak`) to decrease karma of user.

__mod_name__ = "Currency System"

__help__ = """
Currency System[Dalc(Đ)]
 ❍ `/dalc` : To enable / disable Currency system
 ❍ `/dalcstat`: Get stats of waller for your chat
 ❍ Reply message with (`+, +100) to add dalcs to there Wallet.
 ❍ Reply message with (`-, -100`) to snitch dalcs from there Wallet.
"""








