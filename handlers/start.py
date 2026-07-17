from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import create_user
from keyboards.main_keyboard import get_main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    await update.message.reply_text(
        f"Olá, {user.first_name}! 👋\n\n"
        "Bem-vindo ao Achados GERAL!\n\n"
        "Aqui você receberá as melhores promoções automaticamente.\n\n"
        "Clique no botão abaixo para ativar as notificações.",
        reply_markup=get_main_keyboard()
    )