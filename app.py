from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.promotions import subscribe_promotions
from database.init_db import init_database


def main():

    # Inicializa o banco de dados
    init_database()

    # Cria a aplicação do bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Comando /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # Botão inline "🔔 Receber Promoções"
    app.add_handler(
        CallbackQueryHandler(
            subscribe_promotions,
            pattern="^subscribe$"
        )
    )

    print("🤖 Bot iniciado!")

    # Inicia o bot
    app.run_polling()


if __name__ == "__main__":
    main()