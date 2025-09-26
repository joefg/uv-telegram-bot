from functools import wraps


def only_chat(chat_id):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            if update.message.chat.id == int(chat_id):
                return await func(update, context, *args, **kwargs)
            else:
                await update.message.reply_text("Access denied, ask an admin.")

        return wrapper

    return decorator


def only_user(user_id):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            if update.message.from_user.id == int(user_id):
                return await func(update, context, *args, **kwargs)
            else:
                await update.message.reply_text("Access denied, ask an admin.")

        return wrapper

    return decorator
