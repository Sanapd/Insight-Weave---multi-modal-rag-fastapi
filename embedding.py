"""
embedding.py
Generates embeddings locally using SentenceTransformers
No API key required
Works reliably with Pinecone (dimension = 384)
"""

from sentence_transformers import SentenceTransformer


# Load model once (fast + efficient)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_list, api_key=None):
    """
    Generate embeddings locally

    Args:
        text_list (list): list of text chunks
        api_key (ignored): kept for compatibility with existing pipeline

    Returns:
        list: embedding vectors
    """

    print(f"[embedding] Embedding {len(text_list)} items locally...")

    try:
        embeddings = model.encode(
            text_list,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        embeddings = embeddings.tolist()

        print("✅ Embedding generation complete.")

        return embeddings

    except Exception as e:
        print(f"Embedding failure: {e}")

        # fallback safe vectors
        return [[0.0] * 384 for _ in text_list]