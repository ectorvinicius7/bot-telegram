from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Sou o Achados GERAL.\n\n"
        "Vou te ajudar a encontrar ofertas e promoções.\n\n"
        "Use /produtos para ver exemplos de produtos carregados de um arquivo JSON."
    )