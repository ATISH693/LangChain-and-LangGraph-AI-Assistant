from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv("CHECKPOINT_DB_URL")


def get_checkpointer():

    context = PostgresSaver.from_conn_string(DB_URI, prepare_threshold=None)

    checkpointer = context.__enter__()

    return context, checkpointer