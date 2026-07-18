import json
from pathlib import Path
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes


PRODUCTS_FILE = Path(__file__).resolve().parent.parent / "products.json"


def load_products() -> list[dict[str, Any]]:
    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_product(product: dict[str, Any]) -> str:
    return (
        f"📦 {product['name']}\n"
        f"💰 Preço: {product['price']}\n"
        f"📝 {product['description']}\n"
        f"🔗 {product['link']}"
    )


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    products = load_products()

    if not products:
        await update.message.reply_text("Nenhum produto disponível no momento.")
        return

    message = "🛍️ Produtos em destaque:\n\n"
    message += "\n\n".join(format_product(product) for product in products)

    await update.message.reply_text(message)
