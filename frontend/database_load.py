from dotenv import load_dotenv
from psycopg import Connection
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_connection():

    return Connection.connect(
        DB_URL,
        prepare_threshold=None
    )


def save_message(thread_id, title, role, message):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT title
            FROM chat_history
            WHERE thread_id = %s
            LIMIT 1
            """,
            (thread_id,)
        )

        row = cur.fetchone()

        if row:
            title = row[0]
        elif not title:
            title = message

        cur.execute(
            """
            INSERT INTO chat_history
            (thread_id, title, role, message)
            VALUES (%s, %s, %s, %s)
            """,
            (thread_id, title, role, message)
        )

    conn.commit()
    conn.close()


def load_messages(thread_id):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT role, message
            FROM chat_history
            WHERE thread_id = %s
            ORDER BY created_at
            """,
            (thread_id,)
        )

        rows = cur.fetchall()

    conn.close()

    messages = []

    for role, message in rows:

        messages.append(
            {
                "role": role,
                "content": message
            }
        )

    return messages


def load_threads():

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute("""
            SELECT
                thread_id,
                MAX(title) AS title,
                MAX(created_at) AS last_message
            FROM chat_history
            GROUP BY thread_id
            ORDER BY last_message DESC
        """)

        rows = cur.fetchall()

    conn.close()

    return rows


def delete_thread(thread_id):

    conn = get_connection()

    with conn.cursor() as cur:

        cur.execute(
            """
            DELETE FROM chat_history
            WHERE thread_id = %s
            """,
            (thread_id,)
        )

    conn.commit()
    conn.close()