# main.py
import os
import dotenv
from pinecone import Pinecone, ServerlessSpec

# Import pipeline modules
from Read_data import download_blob_data
from img import extract_images_and_caption
from table import extract_tables_to_text
from chunking import extract_text_chunks
from formulas import extract_formulas_and_clean
from embedding import generate_embeddings
from vector_store import upload_to_pinecone

dotenv.load_dotenv()

def run_ingestion(force_refresh=False):
    print("\n--- 🚀 Starting Ingestion Pipeline ---")
    
    # 1. Validation
    required_vars = ["PINECONE_API_KEY", "PINECONE_INDEX_NAME", "GEMINI_API_KEY", "AZURE_CONN_STRING", "AZURE_CONTAINER","AZURE_BLOB_NAME"
    ]
    if not all(os.getenv(k) for k in required_vars):
        print(f"❌ Error: Missing Environment Variables. Check .env")
        return False

    # 2. Connect to Vector DB
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if index_name not in [i.name for i in pc.list_indexes()]:
            print(f"[Pinecone] Creating Index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=768, 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        
        # 3. Smart Skip Logic
        if stats.total_vector_count > 0 and not force_refresh:
            print(f"✅ Database Ready ({stats.total_vector_count} vectors). Skipping ingestion.")
            return True

    except Exception as e:
        print(f"❌ Pinecone Connection Failed: {e}")
        return False

    # 4. Pipeline Execution
    print("📉 Database empty or refresh requested. Downloading Data...")
    
    pdf_bytes = download_blob_data()
    if not pdf_bytes:
        print("❌ Failed to download PDF from Azure.")
        return False

    print("--- 📸 Skipping Image Captioning (Gemini quota exceeded) ---")
    images = []
    
    print("--- 📊 Processing Tables ---")
    tables = extract_tables_to_text(pdf_bytes)
    
    print("--- 📝 Processing Text & Formulas ---")
    text_chunks = extract_text_chunks(pdf_bytes)
    cleaned_text = extract_formulas_and_clean(text_chunks) # Uses your formula.py logic

    # Merge all data types
    all_data = images + tables + cleaned_text
    print(f"--- 📦 Total Chunks to Embed: {len(all_data)} ---")

    if not all_data:
        print("⚠️ No data extracted.")
        return False

    # 5. Embed & Store
    try:
        texts = [d['text'] for d in all_data]
        vectors = generate_embeddings(texts, os.getenv("GEMINI_API_KEY"))
        upload_to_pinecone(all_data, vectors, os.getenv("PINECONE_API_KEY"), index_name)
        print("--- ✅ Ingestion Complete ---")
        return True
    except Exception as e:
        print(f"❌ Embedding/Upload Failed: {e}")
        return False

if __name__ == "__main__":
    run_ingestion(force_refresh=True)