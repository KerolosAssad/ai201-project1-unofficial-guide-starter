import gradio as gr
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response


def run_ingestion():
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Loading documents...")
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    embed_and_store(all_chunks)
    print(f"Ingestion complete. {len(all_chunks)} chunks stored.")


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    retrieved = retrieve(question)
    result = generate_response(question, retrieved)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="violet"),
    title="IndieDev Guide",
) as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#5b21b6; margin:0;">
                🎨 IndieDev Guide
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Advice for indie game artists transitioning from digital art into game development.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            question = gr.Textbox(
                label="Your question",
                placeholder='e.g. "What game engine should I use as an artist with no coding experience?"',
                lines=2,
            )
            btn = gr.Button("Ask", variant="primary")
            answer = gr.Textbox(label="Answer", lines=10, interactive=False)
            sources = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

            btn.click(handle_query, inputs=question, outputs=[answer, sources])
            question.submit(handle_query, inputs=question, outputs=[answer, sources])

        with gr.Column(scale=1, min_width=180):
            gr.HTML("""
            <div style="background:#f5f3ff; border:1px solid #ddd6fe;
                        border-radius:10px; padding:1rem; margin-top:0.5rem;">
                <p style="font-size:0.8rem; font-weight:700; color:#4c1d95;
                        margin:0 0 0.5rem; letter-spacing:0.05em;">
                    📚 LOADED SOURCES
                </p>
                <ul style="font-size:0.85rem; color:#5b21b6; list-style:none;
                            padding:0; margin:0; line-height:2;">
                    <li><a href="https://medium.com/@kuppy_kp_/a-f-cking-long-journal-from-a-ux-designer-who-became-an-indie-game-dev-artist-in-2023-10345a61bbbb" target="_blank" style="color:#5b21b6; text-decoration:none;">✍️ Medium Journal</a></li>
                    <li><a href="https://80.lv/articles/the-journey-from-an-artist-to-a-game-developer" target="_blank" style="color:#5b21b6; text-decoration:none;">🎮 80.lv Interview</a></li>
                    <li><a href="https://www.juegostudio.com/blog/best-tools-for-art-and-design" target="_blank" style="color:#5b21b6; text-decoration:none;">🛠️ Juego Studios Tools</a></li>
                    <li><a href="https://github.com/dawdle-deer/awesome-learn-gamedev" target="_blank" style="color:#5b21b6; text-decoration:none;">📋 Awesome Gamedev</a></li>
                    <li><a href="https://pixune.com/blog/game-art-pipeline/" target="_blank" style="color:#5b21b6; text-decoration:none;">🖼️ Pixune Pipeline</a></li>
                    <li><a href="https://www.reddit.com/r/gamedev/comments/qqbyqo/it_seems_artists_have_an_easier_time_becoming/" target="_blank" style="color:#5b21b6; text-decoration:none;">💬 r/gamedev Thread</a></li>
                    <li><a href="https://www.reddit.com/r/IndieDev/comments/1qf2xn1/solo_dev_struggling_with_artvisuals_how_did_you/" target="_blank" style="color:#5b21b6; text-decoration:none;">💬 r/IndieDev Thread</a></li>
                    <li><a href="https://www.gamedeveloper.com/business/making-it-work-as-a-solo-game-developer" target="_blank" style="color:#5b21b6; text-decoration:none;">📝 Solo Dev Guide</a></li>
                    <li><a href="https://www.gamedeveloper.com/art/illustrators-four-things-your-indie-coder-wants-you-to-know-about-game-art" target="_blank" style="color:#5b21b6; text-decoration:none;">📝 Illustrators Guide</a></li>
                    <li><a href="https://www.creativebloq.com/art/digital-art/how-art-lays-the-foundations-for-indie-games" target="_blank" style="color:#5b21b6; text-decoration:none;">🎨 Creative Bloq</a></li>
                </ul>
                <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                    Answers are grounded in the loaded sources only. If a topic
                    isn't covered, the guide will say so.
                </p>
            </div>
        """)

    gr.Examples(
        examples=[
            "What game engine should I use as an artist with no coding experience?",
            "What art styles are easiest to start with as a beginner?",
            "How do solo devs handle the parts of game dev they're weakest at?",
            "What are the biggest struggles artists face when learning to code?",
            "What kinds of artists transition into indie game development?",
        ],
        inputs=question,
    )


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  IndieDev Guide — starting up")
    print("="*50 + "\n")

    run_ingestion()
    demo.launch()