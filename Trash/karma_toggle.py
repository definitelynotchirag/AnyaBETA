import NekoRobot.modules.mongo.dalc_mongo as ksql

from NekoRobot.modules.sql import log_channel_sql as logsql

import html
from NekoRobot import NEKO_PTB
from telegram import ParseMode

from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ParseMode, Update)

from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler)

from telegram.utils.helpers import mention_html

from NekoRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply

# from NekoRobot import dispatcher

from NekoRobot.modules.log_channel import gloggable, loggable

bot_name = f"{NEKO_PTB.bot.first_name}"

@user_admin_no_reply
@loggable
@gloggable

def karma_status(update: Update, context : CallbackContext):
  query = update.callback_query
  bot = context.bot
  user = update.effective_user
  if query.data == "add_karma":
    chat = update.effective_chat
    is_chatbot = ksql.is_karma(chat.id)
    if not is_chatbot:
        is_chatbot = ksql.set_karma(chat.id)
        LOG = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"CURRENCY_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        log_channel = logsql.get_chat_log_channel(chat.id)
        if log_channel:
                bot.send_message(
                log_channel,
                LOG,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        update.effective_message.edit_text(
                f"{bot_name} Currency System Enabled by {mention_html(user.id, user.first_name)}.",
                parse_mode=ParseMode.HTML,)
        return LOG
    elif is_chatbot:
      return update.effective_message.edit_text(
        f"{bot_name} Currency System Already Enabled.",
                parse_mode=ParseMode.HTML
      )
    else:
            return update.effective_message.edit_text(
                "Error!",
                parse_mode=ParseMode.HTML,
            )


  elif query.data == "rem_karma":
    chat = update.effective_chat
    is_chatbot = ksql.is_karma(chat.id)
    if is_chatbot:
        is_chatbot = ksql.rem_karma(chat.id)
        LOG = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"CURRENCY_DISABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        log_channel = logsql.get_chat_log_channel(chat.id)
        if log_channel:
                bot.send_message(
                log_channel,
                LOG,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        update.effective_message.edit_text(
                f"{bot_name} Currency System disabled by {mention_html(user.id, user.first_name)}.",
                parse_mode=ParseMode.HTML,
            )
        return LOG
    elif not is_chatbot:
        return update.effective_message.edit_text(
              f"{bot_name} Currency System Already Disabled.",
              parse_mode=ParseMode.HTML,
            )
    else:
        return update.effective_message.edit_text(
             "Error!",
            parse_mode=ParseMode.HTML,
        )



@user_admin
@loggable
def karma_toggle(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data=r"add_karma")],
       [
        InlineKeyboardButton(
            text="Disable",
            callback_data=r"rem_karma")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

KARMA_STATUS_HANDLER = CommandHandler("dalc", karma_toggle, run_async = True)
ADD_KARMA_HANDLER = CallbackQueryHandler(karma_status, pattern=r"add_karma", run_async = True)
RM_KARMA_HANDLER = CallbackQueryHandler(karma_status, pattern=r"rem_karma", run_async = True)

NEKO_PTB.add_handler(ADD_KARMA_HANDLER)
NEKO_PTB.add_handler(KARMA_STATUS_HANDLER)
NEKO_PTB.add_handler(RM_KARMA_HANDLER)

__handlers__ = [
    ADD_KARMA_HANDLER,
    KARMA_STATUS_HANDLER,
    RM_KARMA_HANDLER,
]