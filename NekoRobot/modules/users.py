from io import BytesIO
from time import sleep

from telegram import TelegramError, Update , parsemode, ParseMode
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler

import NekoRobot.modules.sql.users_sql as sql
from NekoRobot import DEV_USERS, LOGGER, NEKO_PTB, OWNER_ID
from NekoRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from NekoRobot.modules.sql.users_sql import get_all_users

USERS_GROUP = 4
CHAT_GROUP = 5
DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    if len(users) == 1:
        return users[0].user_id
    for user_obj in users:
        try:
            userdat = NEKO_PTB.bot.get_chat(user_obj.user_id)
            if userdat.username == username:
                return userdat.id

        except BadRequest as excp:
            if excp.message != "Chat not found":
                LOGGER.exception("Error extracting user ID")

    return None


# @dev_plus
# def broadcast(update: Update, context: CallbackContext):
#     to_send = update.effective_message.text.split(None, 1)

#     if len(to_send) >= 2:
#         to_group = False
#         to_user = False
#         if to_send[0] == "/broadcastgroups":
#             to_group = True
#         if to_send[0] == "/broadcastusers":
#             to_user = True
#         else:
#             to_group = to_user = True
#         chats = sql.get_all_chats() or []
#         users = get_all_users()
#         failed = 0
#         failed_user = 0
#         if to_group:
#             for chat in chats:
#                 try:
#                     context.bot.sendMessage(
#                         int(chat.chat_id),
#                         to_send[1],
#                         parse_mode="MARKDOWN",
#                         disable_web_page_preview=True,
#                     )
#                     sleep(0.1)
#                 except TelegramError:
#                     failed += 1
#         if to_user:
#             for user in users:
#                 try:
#                     context.bot.sendMessage(
#                         int(user.user_id),
#                         to_send[1],
#                         parse_mode="MARKDOWN",
#                         disable_web_page_preview=True,
#                     )
#                     sleep(0.1)
#                 except TelegramError:
#                     failed_user += 1
#         update.effective_message.reply_text(
#             f"Broadcast complete.\nGroups failed: {failed}.\nUsers failed: {failed_user}.",
#         )

# @dev_plus
# def broadcast(update: Update, context: CallbackContext):
#     to_send = update.effective_message.text.split(None, 1)
#     replymsg = update.effective_message.reply_to_message
#     if len(to_send) >= 2:
#         if replymsg:
#             # return context.bot.sendMessage(update.effective_chat.id, 'Please reply to a message!')
#             tosendtext = replymsg.text
#         else:
#             tosendtext = to_send[1]
#         to_group = False
#         to_user = False
#         if to_send[0] == "/broadcastgroups":
#             to_group = True
#         if to_send[0] == "/broadcastusers":
#             to_user = True
#         else:
#             to_group = to_user = True
#         chats = sql.get_all_chats() or []
#         users = get_all_users()
#         failed = 0
#         failed_user = 0
#         if to_group:
#             for chat in chats:
#                 try:
#                     context.bot.sendMessage(
#                         int(chat.chat_id),
#                         tosendtext,
#                         parse_mode="MARKDOWN_V2",
#                         disable_web_page_preview=True,
#                     )
#                     sleep(0.1)
#                 except TelegramError:
#                     failed += 1
#         if to_user:
#             for user in users:
#                 try:
#                     context.bot.sendMessage(
#                         int(user.user_id),
#                         tosendtext,
#                         parse_mode="MARKDOWN_V2",
#                         disable_web_page_preview=True,
#                     )
#                     sleep(0.1)
#                 except TelegramError:
#                     failed_user += 1
#         update.effective_message.reply_text(
#             f"Broadcast complete.\nGroups failed: {failed}.\nUsers failed: {failed_user}.",
#         )


from NekoRobot import tbot
from NekoRobot import DEV_USERS, LOGGER, NEKO_PTB, OWNER_ID
from NekoRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from NekoRobot.modules.sql.users_sql import get_all_users
import NekoRobot.modules.sql.users_sql as sql
from telethon.errors.rpcerrorlist import FloodWaitError
import asyncio
from NekoRobot.events import register

DEV_AND_MORE = DEV_USERS
DEV_AND_MORE.append(int(OWNER_ID))
# DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))

@register(pattern="/broadcast")
async def broadcast(event):
    if event.sender_id not in DEV_AND_MORE:
        return
    if event.text == '/broadcastgroups':
        togroup = True
    elif event.text == '/broadcastusers':
        touser = True
    else:
        togroup = touser = True
    replymsg = await event.get_reply_message()
    if not replymsg:
        return await event.reply('Reply to a message.')
    failed = 0
    failed_user = 0
    procmsg = await event.reply('Broadcasting...Please wait.')
    if togroup:
        chats = sql.get_all_chats() or []
        for chat in chats:
            try:
                await tbot.send_message(int(chat.chat_id), replymsg, link_preview=False)
                await asyncio.sleep(0.1)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except:
                failed += 1
                pass
    if touser:
        users = get_all_users()
        for user in users:
            try:
                await tbot.send_message(int(user.user_id), replymsg, link_preview=False)
                await asyncio.sleep(0.1)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except:
                failed_user += 1
                pass
    return await procmsg.edit(f"Broadcast complete.\nGroups failed: {failed}.\nUsers failed: {failed_user}.")
 


def log_user(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message

    sql.update_user(msg.from_user.id, msg.from_user.username, chat.id, chat.title)

    if msg.reply_to_message:
        sql.update_user(
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
            chat.id,
            chat.title,
        )

    if msg.forward_from:
        sql.update_user(msg.forward_from.id, msg.forward_from.username)


@sudo_plus
def chats(update: Update, context: CallbackContext):
    all_chats = sql.get_all_chats() or []
    chatfile = "List of chats.\n0. Chat name | Chat ID | Members count\n"
    P = 1
    for chat in all_chats:
        try:
            curr_chat = context.bot.getChat(chat.chat_id)
            curr_chat.get_member(context.bot.id)
            chat_members = curr_chat.get_member_count(context.bot.id)
            chatfile += "{}. {} | {} | {}\n".format(
                P,
                chat.chat_name,
                chat.chat_id,
                chat_members,
            )
            P += 1
        except:
            pass

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "groups_list.txt"
        update.effective_message.reply_document(
            document=output,
            filename="groups_list.txt",
            caption="Here be the list of groups in my database.",
        )


def chat_checker(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if update.effective_message.chat.get_member(bot.id).can_send_messages is False:
            bot.leaveChat(update.effective_message.chat.id)
    except Unauthorized:
        pass


def __user_info__(user_id):
    if user_id in [777000, 1087968824]:
        return """╘══「 Groups count: <code>???</code> 」"""
    if user_id == NEKO_PTB.bot.id:
        return """╘══「 Groups count: <code>???</code> 」"""
    num_chats = sql.get_user_num_chats(user_id)
    return f"""╘══「 Groups count: <code>{num_chats}</code> 」"""


def __stats__():
    return f"• {sql.num_users()} users, across {sql.num_chats()} chats"


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


# BROADCAST_HANDLER = CommandHandler(
#     ["broadcastall", "broadcastusers", "broadcastgroups"],
#     broadcast,
#     run_async=True,
# )
USER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, log_user, run_async=True
)
CHAT_CHECKER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, chat_checker, run_async=True
)
CHATLIST_HANDLER = CommandHandler("groups", chats, run_async=True)

NEKO_PTB.add_handler(USER_HANDLER, USERS_GROUP)
# NEKO_PTB.add_handler(BROADCAST_HANDLER)
NEKO_PTB.add_handler(CHATLIST_HANDLER)
NEKO_PTB.add_handler(CHAT_CHECKER_HANDLER, CHAT_GROUP)

__mod_name__ = "Users"

__handlers__ = [(USER_HANDLER, USERS_GROUP), CHATLIST_HANDLER]
