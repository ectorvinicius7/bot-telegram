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