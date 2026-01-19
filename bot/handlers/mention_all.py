from telegram import Update, MessageEntity
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.storage import get_users


async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.entities:
        return

    bot_id = context.bot.id

    mentioned = False

    for entity in message.entities:
        if entity.type == MessageEntity.MENTION:
            mention_text = message.text[
                entity.offset : entity.offset + entity.length
            ]
            if mention_text == f"@{context.bot.username}":
                mentioned = True

        elif entity.type == MessageEntity.TEXT_MENTION:
            if entity.user and entity.user.id == bot_id:
                mentioned = True

    if not mentioned:
        return

    chat_id = update.effective_chat.id
    users = get_users(chat_id)

    if not users:
        await message.reply_text("Я пока никого не знаю в этом чате 😢")
        return

    mentions = [
        f'<a href="tg://user?id={user_id}">•</a>'
        for user_id in users
    ]

    await message.reply_text(
        "🔔 Внимание всем:\n" + " ".join(mentions),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
