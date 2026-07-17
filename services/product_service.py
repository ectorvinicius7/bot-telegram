from database.database import get_connection


def create_product(
    name,
    price_current,
    price_old,
    discount,
    url,
    store
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (
            name,
            price_current,
            price_old,
            discount,
            url,
            store
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        price_current,
        price_old,
        discount,
        url,
        store
    ))

    conn.commit()
    conn.close()