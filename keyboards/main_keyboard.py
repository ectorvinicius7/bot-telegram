from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "🔔 Receber Promoções",
                callback_data="subscribe"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)