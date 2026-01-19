from telegram import Update
from telegram.ext import ContextTypes

from bot.storage import add_user


async def track_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    member = update.chat_member

    if not chat or not member:
        return

    user = member.new_chat_member.user
    if not user or user.is_bot:
        return

    add_user(chat.id, user.id)
