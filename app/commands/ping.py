from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from auth.chat import only_user
import config
from models import ping as ping_model

@only_user(config.DEV_CHAT)
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ret = ping_model.ping()
    await update.message.reply_text(ret)

ping_handler = CommandHandler("ping", ping_cmd)
