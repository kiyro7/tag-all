import os
from dotenv import load_dotenv
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functools import wraps
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder

from bot.protected_handlers import *

app = FastAPI()

telegram_app = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Поздороваться снова")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Привет! Я ваш бот. Как я могу помочь?", reply_markup=reply_markup)


async def greet_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Поздороваться снова":
        await update.message.reply_text("Привет! Я ваш бот. Как я могу помочь?")


# Запуск Telegram-бота при старте FastAPI
@app.on_event("startup")
async def start_bot():
    if os.getenv("RUN_MAIN") != "true":
        return
    global telegram_app
    telegram_app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    telegram_app.add_handler(ProtectedCommandHandler("start", start))
    telegram_app.add_handler(ProtectedMessageHandler(filters.TEXT & ~filters.COMMAND, greet_again))

    # запуск в фоне
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()


@app.on_event("shutdown")
async def shutdown_bot():
    global telegram_app
    await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()
