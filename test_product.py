from database.init_db import init_database
from services.product_service import create_product


init_database()


create_product(
    "Mouse Logitech G203",
    89.90,
    159.90,
    44,
    "https://link-do-produto.com",
    "Mercado Livre"
)

print("Produto cadastrado!")