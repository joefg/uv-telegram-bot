from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from models import user as user_model

def new_user_message(user: user_model.User):
    username = f"{user.first_name + (user.last_name or '')}"
    return "\n".join((
        rf"<strong>Hi, {username}!</strong>",
        "",
        rf"You started using this bot on {user.creation_date}."
    ))

def existing_user_message(user: user_model.User):
    username = f"{user.first_name + (user.last_name or '')}"
    return "\n".join((
        rf"<strong>Welcome back, {username}!</strong>",
        "",
        rf"You started using this bot on {user.creation_date}."
    ))

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def register_and_get_user(user_id, first_name, last_name):
        user_model.register_user(user_id, first_name, last_name)
        user = user_model.get_user(user_id)
        return user

    if not update.message: raise Exception("No message")

    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name or None

    user = user_model.get_user(user_id)
    if user:
        await update.message.reply_html(existing_user_message(user))
    else:
        new_user = register_and_get_user(user_id, first_name, last_name)
        await update.message.reply_html(new_user_message(new_user))

start_handler = CommandHandler("start", start_cmd)