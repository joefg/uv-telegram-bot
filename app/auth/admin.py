from functools import wraps

import models.user as users_model

def only_admin(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = users_model.get_user(update.message.from_user.id)
        if not user: return await update.message.reply_text("Access denied")
        if bool(user.is_admin): return await func(update, context, *args, **kwargs)
        else: return await update.message.reply_text("Access denied, ask an admin.")
    return wrapper
