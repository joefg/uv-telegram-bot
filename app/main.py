from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler,
    filters
)

import logging

from commands.help import help_handler
from commands.ping import ping_handler
from commands.start import start_handler

from conversations.account import account_handler

import config
import db.database as database
from error import error_handler

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=(logging.DEBUG if config.DEBUG else logging.INFO)
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    return logger

def setup_app():
    app = Application.builder().token(config.TG_TOKEN).build()
    app.add_handlers(
        [
            help_handler,
            start_handler,
            ping_handler,
            account_handler
        ]
    )
    app.add_error_handler(error_handler)
    return app

if __name__ == '__main__':
    logger = setup_logging()
    database.db.migrate()
    app = setup_app()
    app.run_polling(allowed_updates=Update.ALL_TYPES)
