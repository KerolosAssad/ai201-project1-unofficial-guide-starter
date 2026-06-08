from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved chunks about indie game
    development for artists transitioning from digital art to game dev.

    retrieved_chunks is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "source"   : the source document name
      - "distance" : similarity score (lower = more relevant)

    Returns a dict with:
      - "answer"  : the grounded response string
      - "sources" : list of source document names used
    """
    # Filtering out weak matches
    retrieved_chunks = [c for c in retrieved_chunks if c["distance"] < 0.55]

    if not retrieved_chunks:
        return {
            "answer": (
                "I couldn't find anything relevant in the loaded documents. "
                "Try rephrasing your question or asking something more specific "
                "about transitioning from digital art into indie game development."
            ),
            "sources": []
        }

    

    # Build context block from retrieved chunks
    context = ""
    for chunk in retrieved_chunks:
        context += f"[{chunk['source']}]\n"
        context += chunk["text"]
        context += "\n---\n"

    # Collect unique sources for programmatic attribution
    sources = list(dict.fromkeys(chunk["source"] for chunk in retrieved_chunks))

    messages = [
        {
            "role": "system",
            "content": (
            "You are a helpful guide for indie game artists transitioning from "
            "digital art into game development. "
            "Answer using ONLY the document chunks provided below. "
            "Use all relevant information across the chunks to construct your answer, "
            "even if no single chunk contains the complete answer. "
            "Do not use your general knowledge or training data to fill in gaps. "
            "If the provided chunks genuinely contain no relevant information at all, say: "
            "'I don't have enough information on that in my current sources.' "
            "If you don't have enough information, do not list any sources. "
            "Do not speculate or invent information. "
            "Keep your answer focused and practical. "
            "At the very end of your response, on a new line, write exactly: "
            "SOURCES_USED: followed by a comma-separated list of only the source names "
            "you actually drew from to write your answer. Example: "
            "SOURCES_USED: 01 Medium Ux Designer Journal, 08 Gamedeveloper Solo Dev"
            )
        },
        {
            "role": "user",
            "content": f"Document chunks:\n{context}\n\nQuestion: {query}"
        }
    ]

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }