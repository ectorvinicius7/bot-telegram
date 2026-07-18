from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from handlers.products import products
from handlers.start import start


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("produtos", products))

    print("🤖 Bot iniciado!")

    app.run_polling()


if __name__ == "__main__":
    main()

# python app.py (para inciar o bot)