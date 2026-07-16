from sentence_transformers import SentenceTransformer
import os 

MODEL_PATH = "/app/models/bge-small-en-v1.5"

os.makedirs(
    "/app/models",
    exist_ok=True
)

print("Downloading model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

model.save(MODEL_PATH)

print("Saved:", MODEL_PATH)