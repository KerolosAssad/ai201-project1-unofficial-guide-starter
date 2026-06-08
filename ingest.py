import os
from config import DOCS_PATH


def load_documents():
    """Load all .txt documents from the documents folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            source_name = filename.replace(".txt", "").replace("_", " ").title()
            documents.append({
                "source": source_name,
                "filename": filename,
                "text": text,
            })
    print(f"Loaded {len(documents)} document(s): {[d['source'] for d in documents]}")
    return documents


def chunk_document(text, source_name):
    """
    Split a document into chunks for embedding.

    Strategy: paragraph-aware grouping with overlap.
    - chunk_size = 300 characters: max chunk size, arrived at through testing —
        larger chunks diluted the embedding signal by mixing multiple topics,
        while smaller chunks lacked enough semantic signal; 300 characters
        balances focus and completeness
    - overlap = 20 characters: the last 20 characters of each chunk are
        prepended to the next chunk, ensuring context carries over at
        boundaries without cutting off mid-idea
    - min_length = 100 characters: filters out very short fragments that
        carry insufficient semantic signal for embedding
    - paragraphs are grouped together until hitting chunk_size, ensuring
        chunks respect paragraph boundaries and avoid mid-sentence cuts
    """
    chunk_size = 300
    overlap = 20
    min_length = 100

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    prefix = source_name.lower().replace(" ", "_")
    counter = 0
    current = ""
    last_tail = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= chunk_size:
            current += ("\n\n" if current else "") + paragraph
        else:
            if len(current) >= min_length:
                chunks.append({
                    "text": current.strip(),
                    "source": source_name,
                    "chunk_id": f"{prefix}_{counter}",
                })
                counter += 1
                last_tail = current[-overlap:]
            current = last_tail + "\n\n" + paragraph if last_tail else paragraph

    # The last chunk
    if len(current) >= min_length:
        chunks.append({
            "text": current.strip(),
            "source": source_name,
            "chunk_id": f"{prefix}_{counter}",
        })

    return chunks
