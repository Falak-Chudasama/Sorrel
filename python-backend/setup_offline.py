from sentence_transformers import SentenceTransformer
import os

print("Fetching model and saving strictly to local directory...")
model = SentenceTransformer("BAAI/bge-large-en-v1.5")
model.save("./local_models/bge-large-en-v1.5")
print("Done! You can delete this script.")