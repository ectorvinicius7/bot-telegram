from telegram import Update
from telegram.ext import ContextTypes

from services.user_service import subscribe_user


async def subscribe_promotions(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    subscribe_user(user.id)

    await query.message.reply_text(
        "✅ Inscrição realizada!\n\n"
        "A partir de agora você receberá todas as promoções publicadas."
    )