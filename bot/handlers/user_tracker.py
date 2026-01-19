from telegram import Update
from telegram.ext import ContextTypes

from bot.storage import add_user


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or not update.effective_user:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    add_user(chat_id, user_id)
