from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
from psycopg import Connection
import os

load_dotenv()

DB_URI = os.getenv("CHECKPOINT_DB_URL")


def get_checkpointer():

    conn = Connection.connect(
        DB_URI,
        prepare_threshold=None
    )

    checkpointer = PostgresSaver(conn)

    checkpointer.setup()

    return conn, checkpointer