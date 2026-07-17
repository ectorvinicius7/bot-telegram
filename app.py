from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from handlers.start import start
from database.init_db import init_database


def main():

    # Inicializa o banco de dados
    init_database()

    # Cria a aplicação do bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Registra os comandos
    app.add_handler(
        CommandHandler("start", start)
    )

    print("🤖 Bot iniciado!")

    # Inicia o bot
    app.run_polling()


if __name__ == "__main__":
    main()

# python app.py