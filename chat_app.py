from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq

import os
import re


# Load embedding model once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


async def get_response(query, pc_key, idx_name, gemini_key=None):

    # Connect Pinecone
    pc = Pinecone(api_key=pc_key)
    index = pc.Index(idx_name)

    # Connect Groq
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Retrieval logic
    search_query = query
    retrieval_limit = 5

    if "how many" in query.lower() and "ref" in query.lower():
        retrieval_limit = 10
        search_query += " references bibliography list author title year"

    # Embed query
    q_emb = embed_model.encode(search_query).tolist()

    # Query Pinecone
    results = index.query(
        vector=q_emb,
        top_k=retrieval_limit,
        include_metadata=True
    )

    context_text = ""
    candidate_images = {}

    for match in results["matches"]:

        meta = match["metadata"]
        text = meta.get("text", "")
        m_type = meta.get("type", "text")
        page = meta.get("page", "N/A")

        if m_type == "image":

            path = meta.get("image_path")

            if path:
                filename = os.path.basename(path)
                candidate_images[filename] = path

                context_text += (
                    f"\n[IMAGE AVAILABLE]: {filename} "
                    f"(Description: {text})\n"
                )

        elif m_type == "table":

            context_text += (
                f"\n[TABLE DATA - Page {page}]:\n{text}\n"
            )

        else:

            context_text += (
                f"\n[TEXT Page {page}]: {text}\n"
            )

    # Limit context length
    context_text = context_text[:3000]

    prompt = f"""
You are a research assistant.

Answer ONLY using this context:

{context_text}

Question:
{query}

Rules:
- Convert tables into markdown
- Add citations like [Source: Page X]
- Show images only if explicitly requested
"""

    # Groq LLaMA-3 response
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_answer = response.choices[0].message.content

    # Extract images if requested
    images_to_show = []

    tag_match = re.search(
        r"<<SHOW_IMAGES>>(.*?)<</SHOW_IMAGES>>",
        raw_answer,
        re.DOTALL
    )

    if tag_match:

        filenames = tag_match.group(1).split(",")

        for fname in filenames:
            fname = fname.strip()

            if fname in candidate_images:
                images_to_show.append(candidate_images[fname])

        raw_answer = raw_answer.replace(tag_match.group(0), "")

    return raw_answer.strip(), images_to_show