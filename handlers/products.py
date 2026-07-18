import asyncio
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from telegram import Update
from telegram.ext import ContextTypes


PRODUCTS_FILE = Path(__file__).resolve().parent.parent / "products.json"
MAX_MESSAGE_LENGTH = 3500


def load_products() -> list[dict[str, Any]]:
    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _clean_url(url: str) -> str:
    parsed = urlparse(url)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    filtered_params = [
        (key, value)
        for key, value in query_params
        if key.lower() not in {
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "ref",
            "tag",
            "sp",
            "source",
            "sr",
            "ascsubtag",
            "ls",
            "cmpid",
            "smid",
            "link_code",
            "campaign",
            "ad_id",
            "gclid",
            "fbclid",
        }
    ]
    cleaned = parsed._replace(query=urlencode(filtered_params, doseq=True))
    return urlunparse(cleaned)


def format_product(product: dict[str, Any]) -> str:
    clean_link = _clean_url(str(product.get("link", "")))
    return (
        f"📦 {product['name']}\n"
        f"💰 Preço: {product['price']}\n"
        f"📝 {product['description']}\n"
        f"🔗 {clean_link}"
    )


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    products = load_products()

    if not products:
        await update.message.reply_text("Nenhum produto disponível no momento.")
        return

    await update.message.reply_text("🛍️ Produtos em destaque:")

    for index, product in enumerate(products, start=1):
        formatted = format_product(product)
        await update.message.reply_text(formatted)
        if index < len(products):
            await asyncio.sleep(5)
