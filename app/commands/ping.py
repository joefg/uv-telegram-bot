from telegram import Update
from telegram.ext import ContextTypes

from models import ping as ping_model

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ret = ping_model.ping()
    await update.message.reply_text(ret)
