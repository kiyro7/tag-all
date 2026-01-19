from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from telegram import Update
from functools import wraps
from copy import deepcopy


def username_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if user and user.username:
            return await func(update, context, *args, **kwargs)
        await update.message.reply_text("⛔ Установи username в Telegram чтобы продолжить пользоваться ботом\nДля этого открой настройки и установите имя пользователя")
    return wrapper


class ProtectedCommandHandler(CommandHandler):
    def __init__(self, *args, **kwargs):
        callback = username_required(args[1])
        super().__init__(args[0], callback, *args[2:], **kwargs)


class ProtectedMessageHandler(MessageHandler):
    def __init__(self, *args, **kwargs):
        callback = username_required(args[1])
        super().__init__(args[0], callback, *args[2:], **kwargs)


class ProtectedCallbackQueryHandler(CallbackQueryHandler):
    def __init__(self, *args, **kwargs):
        if args:
            # Если callback передан как первый позиционный аргумент
            callback = username_required(args[0])
            args = (callback, *args[1:])
        elif "callback" in kwargs:
            # Если callback передан как именованный аргумент
            kwargs["callback"] = username_required(kwargs["callback"])
        else:
            raise ValueError("Callback function must be provided for CallbackQueryHandler")

        super().__init__(*args, **kwargs)


class ProtectedConversationHandler(ConversationHandler):
    def __init__(self, *args, **kwargs):
        # Клонируем и оборачиваем callbacks
        protected_entry_points = self._wrap_handlers(kwargs.get("entry_points", []))
        protected_fallbacks = self._wrap_handlers(kwargs.get("fallbacks", []))
        protected_states = {
            state: self._wrap_handlers(handler_list)
            for state, handler_list in kwargs.get("states", {}).items()
        }

        super().__init__(
            entry_points=protected_entry_points,
            states=protected_states,
            fallbacks=protected_fallbacks,
            name=kwargs.get("name"),
            persistent=kwargs.get("persistent", False),
            allow_reentry=kwargs.get("allow_reentry", False),
            conversation_timeout=kwargs.get("conversation_timeout", None),
            per_user=kwargs.get("per_user", True),
            per_chat=kwargs.get("per_chat", True),
            per_message=kwargs.get("per_message", False),
        )

    @staticmethod
    def _wrap_handlers(handlers):
        wrapped = []
        for handler in handlers:
            handler = deepcopy(handler)
            if hasattr(handler, "callback"):
                handler.callback = username_required(handler.callback)
            wrapped.append(handler)
        return wrapped
