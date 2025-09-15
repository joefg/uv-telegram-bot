from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

HELP_TEXT = """
<strong>joefg's bot</strong>

<em>Commands</em>

<code>/ping</code>: Returns "Pong!"
"""

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(HELP_TEXT)
