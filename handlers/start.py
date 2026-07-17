from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import create_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    await update.message.reply_text(
        f"Olá, {user.first_name}! 👋"
    )