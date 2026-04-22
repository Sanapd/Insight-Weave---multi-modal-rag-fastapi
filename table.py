# table.py
import pdfplumber
import io

def extract_tables_to_text(pdf_bytes):
    """
    Extracts tables and converts them to Markdown for the LLM.
    Replaces 'camelot' to remove Ghostscript dependency for cloud compatibility.
    """
    if not pdf_bytes: return []
    
    processed_tables = []
    
    try:
        # Open the PDF bytes directly
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table in tables:
                    # Skip empty or tiny tables (noise)
                    if not table or len(table) < 2: 
                        continue
                    
                    # Clean None values and sanitize
                    clean_table = [[str(cell).replace('\n', ' ') if cell else "" for cell in row] for row in table]
                    
                    # Convert to Markdown Table format (Best for LLM readability)
                    # | Header 1 | Header 2 |
                    header = " | ".join(clean_table[0])
                    separator = " | ".join(["---"] * len(clean_table[0]))
                    rows = "\n".join([" | ".join(row) for row in clean_table[1:]])
                    
                    markdown_table = f"{header}\n{separator}\n{rows}"
                    
                    processed_tables.append({
                        "text": f"[TABLE DATA - Page {page_num + 1}]:\n{markdown_table}",
                        "type": "table",
                        "page": page_num + 1,
                        "image_path": ""
                    })
        
        print(f"[table] Extracted {len(processed_tables)} tables successfully.")

    except Exception as e:
        print(f"⚠️ [Table] Extraction warning: {e}")
        return []

    return processed_tables