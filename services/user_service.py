from database.database import get_connection


def create_user(telegram_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (
            telegram_id,
            username,
            first_name
        )
        VALUES (?, ?, ?)
    """, (
        telegram_id,
        username,
        first_name
    ))

    conn.commit()
    conn.close()


def subscribe_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET is_subscribed = 1
        WHERE telegram_id = ?
    """, (telegram_id,))

    conn.commit()
    conn.close()