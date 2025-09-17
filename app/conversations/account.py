from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import (
    CommandHandler, ContextTypes, ConversationHandler, MessageHandler,
    filters
)
import logging
import models.user as user_model

MENU, SHOW, UPDATE, CONFIRM_DELETE = range(4)
BUTTONS = [
    ["/show", "/update", "/delete"],
    ["/done"]
]

async def menu_account_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MENU_MSG = f"""
<strong>Your Account</strong>

Please select an option using the buttons.
"""
    await update.message.reply_html(
        MENU_MSG,
        reply_markup=ReplyKeyboardMarkup(
            BUTTONS
        )
    )
    return MENU

async def show_account_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def account_details(user: user_model.User) -> str:
        return f"""
<strong>Your account:</strong>

Telegram ID: {user.telegram_id}
First name: {user.first_name}
{('Last name: ' + user.last_name) if user.last_name else ''}
Created on: {user.creation_date}

---

{"Account active" if user.is_active else "Account inactive"}
{"<strong>This user is an administrator</strong>" if user.is_admin else ""}
 """

    user_id = update.message.from_user.id
    user = user_model.get_user(user_id)
    if user:
        await update.message.reply_html(account_details(user))
    return MENU

async def update_account_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UPDATE_USER_MSG = f"""
<strong>User account updated.</strong>

Please note that this bot uses the account details
associated with your Telegram account.
    """
    if not update.message: raise Exception("No message")

    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name or ""

    user = user_model.get_user(user_id)
    if user:
        user_model.update_user(user.id, first_name, last_name)
        await update.message.reply_html(UPDATE_USER_MSG)
    return MENU

async def delete_account_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DELETE_USER_MSG = f"""
<strong>User account deleted.</strong>

Thank you for using this bot!
    """

    if not update.message: raise Exception("No message")

    user_id = update.message.from_user.id
    user = user_model.get_user(user_id)

    if user:
        user_model.delete_user(user.id)
        await update.message.reply_html(DELETE_USER_MSG)
    return ConversationHandler.END

async def confirm_delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CONFIRM_USER_MSG = f"""
<strong>Are you sure you want to do this?</strong>

Please select your choice via the keyboard buttons.
    """
    BUTTONS = [["Yes", "No"]]
    await update.message.reply_html(
        CONFIRM_USER_MSG,
        reply_markup=ReplyKeyboardMarkup(BUTTONS)
    )
    return CONFIRM_DELETE

async def no_delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    NO_DELETE_USER_MSG = f"""
<strong>Account not deleted.</strong>
    """
    await update.message.reply_html(
        NO_DELETE_USER_MSG,
        reply_markup=ReplyKeyboardMarkup(BUTTONS)
    )
    return MENU

async def done_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DONE_USER_CMD = f"""
<strong>Done.</strong>
    """
    await update.message.reply_html(
        DONE_USER_CMD,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

account_handler = ConversationHandler(
    entry_points=[CommandHandler("account", menu_account_cmd)],
    states={
        MENU: [
            CommandHandler("show", show_account_cmd),
            CommandHandler("update", update_account_cmd),
            CommandHandler("delete", confirm_delete_cmd)
        ],
        SHOW: [
            CommandHandler("show", show_account_cmd),
            CommandHandler("update", update_account_cmd),
            CommandHandler("delete", confirm_delete_cmd)
        ],
        UPDATE: [
            CommandHandler("show", show_account_cmd),
            CommandHandler("update", update_account_cmd),
            CommandHandler("delete", confirm_delete_cmd)
        ],
        CONFIRM_DELETE: [
            MessageHandler(filters.Regex("Yes"), delete_account_cmd),
            MessageHandler(filters.Regex("No"), no_delete_cmd)
        ]
    },
    fallbacks=[
        CommandHandler("done", done_cmd)
    ]
)
