# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Indie game artists transitioning from digital art into game development — useful because most resources assume a programming background, and the advice that actually helps artist-first developers is scattered across blogs, Reddit threads, and postmortems with no single place to find it.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Medium | Year-long journal from a UX designer with zero coding experience learning pixel art and game dev from scratch | https://medium.com/@kuppy_kp_/a-f-cking-long-journal-from-a-ux-designer-who-became-an-indie-game-dev-artist-in-2023-10345a61bbbb |
| 2 | 80.lv | In-depth interview with a developer who made the full switch from game artist to indie dev, covering tools, pipelines, and engine choices | https://80.lv/articles/the-journey-from-an-artist-to-a-game-developer |
| 3 | Juego Studios | Covers Photoshop, Clip Studio Paint, and Aseprite and how each fits into an indie game art workflow | https://www.juegostudio.com/blog/best-tools-for-art-and-design |
| 4 |  GitHub | Curated resource list with sections on art-to-tech topics: shader guides, tech art courses, and VFX pipelines | https://github.com/dawdle-deer/awesome-learn-gamedev  |
| 5 | pixune.com | Detailed breakdown of the full game art pipeline from concept art through animation, texturing, and engine integration | https://pixune.com/blog/game-art-pipeline/ |
| 6 | r/gamedev |Reddit thread where a programmer vents about the difficulty of learning art as a non-artist, generating a long community discussion covering free vs. paid tools, learning resources, the art vs. programming learning curve debate, and practical advice for getting passable game art without formal training. | https://www.reddit.com/r/gamedev/comments/qqbyqo/it_seems_artists_have_an_easier_time_becoming/ |
| 7 | r/IndieDev | Thread where a solo developer with zero art background asks how others tackled visuals, generating detailed responses covering style choices (low-poly, pixel art), shader-based workarounds, hiring artists, using asset packs coherently, and a developer's firsthand account of going from terrible programmer art to a polished visual style over 1.5 years with no art training. |  https://www.reddit.com/r/IndieDev/comments/1qf2xn1/solo_dev_struggling_with_artvisuals_how_did_you/ |
| 8 | gamedeveloper.com | Long-form blog post from a solo dev who came from a game artist background and had to learn coding, giving a rare flip-side perspective on the art/code divide | https://www.gamedeveloper.com/business/making-it-work-as-a-solo-game-developer |
| 9 | gamedeveloper.com | A startup guide written specifically for illustrators and classically trained artists moving into game asset creation - covering the key constraints, workflow differences, and mindset shifts that trip up artists coming from a fine art or freelance illustration background. | https://www.gamedeveloper.com/art/illustrators-four-things-your-indie-coder-wants-you-to-know-about-game-art |
| 10 | Creative Bloq | Five indie game artists explain how their visual background directly shaped the worlds, stories, and emotions of their games — covering art direction, style development, and how artistic choices drive gameplay decisions, all from an artist-first perspective. | https://www.creativebloq.com/art/digital-art/how-art-lays-the-foundations-for-indie-games |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

300 characters

**Overlap:**

20 characters

**Why these choices fit your documents:**

The documents are conversational and fragmented; knowledge is spread across short statements in Reddit threads, interview answers, and blog paragraphs rather than concentrated in long passages. Initial testing with 1000-character chunks showed the embedding signal being diluted by mixing multiple topics within a single chunk, causing retrieval to return loosely related content. Reducing to 300 characters with paragraph-aware grouping produced tighter, more focused chunks that embed more accurately. Paragraphs are grouped sequentially until hitting the 300-character limit, ensuring chunks always respect paragraph boundaries and avoid mid-sentence cuts. A 20-character overlap prepends the tail of each chunk to the next, preserving context at boundaries. Documents were preprocessed before chunking; where Reddit UI elements (upvote/downvote buttons, usernames, timestamps, share buttons), Medium subscription prompts, image caption artifacts, and off-topic sections were manually removed from all 10 source documents.


**Final chunk count:**

385 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

`all-MiniLM-L6-v2` via `sentence-transformers` — chosen because it runs locally with no API key or rate limits, is fast and lightweight, and performs well on short to medium English text which matches the conversational nature of the corpus. It was also the model used in the CodePath Tinker Lab, making it a familiar and well-understood starting point for this project.

**Production tradeoff reflection:**

If deploying for real users without cost constraints, I would consider `text-embedding-3-large` (OpenAI) or `embed-english-v3.0` (Cohere) for better accuracy on domain-specific language. The indie game art domain mixes technical game dev vocabulary with artistic terminology; where a larger, more capable model would handle that intersection more reliably than `all-MiniLM-L6-v2`, which is optimized for speed over nuance. Context length would also be a factor: some chunks from interview-style documents carry meaning across multiple sentences, and a model with a larger context window would embed those more faithfully. The main tradeoffs are latency and cost; and larger API-hosted models are slower and more expensive than a locally-run model, so for a production system I would benchmark retrieval quality against response time and likely land on a mid-tier model like `text-embedding-3-small` as a balance between accuracy and speed.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The LLM is instructed to answer using only the provided document chunks and explicitly forbidden from drawing on general knowledge or training data. The exact instruction passed to the model is:

*"You are a helpful guide for indie game artists transitioning from digital art into game development. Answer using ONLY the document chunks provided below. Use all relevant information across the chunks to construct your answer, even if no single chunk contains the complete answer. Do not use your general knowledge or training data to fill in gaps. If the provided chunks genuinely contain no relevant information at all, say: 'I don't have enough information on that in my current sources.' If you don't have enough information, do not list any sources. Do not speculate or invent information. Keep your answer focused and practical. At the very end of your response, on a new line, write exactly: SOURCES_USED: followed by a comma-separated list of only the source names you actually drew from to write your answer. Example: SOURCES_USED: 01 Medium Ux Designer Journal, 08 Gamedeveloper Solo Dev"*

In addition to the system prompt, low-relevance chunks are filtered out before being passed to the LLM; where any chunk with a distance score above 0.55 is discarded, ensuring the model only sees chunks that are semantically close to the query. If filtering removes all chunks, the system returns the "not enough information" response without calling the LLM at all.

**How source attribution is surfaced in the response:**

The LLM is instructed to append a `SOURCES_USED:` line listing only the sources it actually drew from and not all the chunks' sources, these are displayed in the UI at the bottom separate from the answer. 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What kinds of artists or designers transition into indie game development? | UX designers, illustrators, 3D artists, concept artists, and traditional fine artists; each bringing different strengths and facing different technical gaps [Medium, 80.lv, gamedeveloper.com #9] | Talented artists from various categories, including illustrators and "classically trained" artists, can transition into indie game development. These artists may come from different backgrounds and may not necessarily have experience in game development, but they can still contribute to the creation of in-game assets and influence game worlds, stories, and emotions. | Partially relevant | Partially accurate |
| 2 | What game engines do artist-first developers most commonly recommend for beginners with no coding background? | Godot is frequently recommended for its free, lightweight nature and beginner-friendly GDScript; other engines are chosen based on project type rather than one-size-fits-all [Medium, 80.lv, r/IndieDev] | As an artist with no coding experience, you should consider a game engine that is lightweight, free, and has a great community, such as Godot. This engine is a good choice because it allows you to build your game without requiring you to write code, although it's still important to understand how computers speak and work with building blocks. | Relevant | Accurate |
| 3 | What are the biggest struggles artists face when learning to code for game development? | Moving from visual thinking to logic-based programming, choosing the right engine, and the lack of structured learning paths designed for artists rather than programmers [r/gamedev, r/IndieDev, gamedeveloper.com #8] | The biggest struggles artists face when learning to code are transitioning from an environment with loose constraints to one with strict coding requirements, and understanding the differences in concept implementation between art and programming. Artists are used to operating in environments with fewer constraints, whereas coding requires precise implementation. Additionally, the abundance of mediocre-to-bad coding tutorials can make it difficult for artists to learn good coding practices. Artists may also struggle with the fact that bad code is not as visible as bad art, making it harder to compare and improve. Furthermore, artists may need to perform a variety of tasks that require different art styles and techniques, which can be equally demanding. | Relevant | Accurate |
| 4 | How do solo indie developers with an art background handle the parts of game dev they're weakest at? | Common strategies include collaborating with a programmer, using visual scripting tools, leaning into art-heavy styles that minimize complex code, or spending dedicated time learning one engine deeply [r/IndieDev, gamedeveloper.com #8, gamedeveloper.com #9] | To handle the parts of game development they're weakest at, solo devs may need to adopt a mindset that allows them to navigate unfamiliar areas. Since solo devs often work with minimal partners, such as publishers or contractors, they may need to learn to manage these relationships effectively to stay afloat. Given the lack of stability in the game development industry, solo devs might need to be adaptable and willing to take on new challenges, even if it means working outside their area of expertise. This could involve collaborating with others who have strengths in areas where the solo dev is weak, or finding ways to learn and improve their skills in those areas. | Partially relevant | Partially accurate |
| 5 | What art styles are most recommended for artists transitioning into game dev with limited technical resources? | Low-poly, pixel art, and minimalist styles are consistently recommended as forgiving and achievable; tool choices like Aseprite and Clip Studio Paint are highlighted for artists already comfortable with digital tools [r/IndieDev, Juego Studios, pixune.com, Creative Bloq] | As a beginner, it's recommended to start with simpler art styles such as low poly, pixel art, or hand-drawn. These styles require less time and can still produce cute or funny results, making them more forgiving for those without extensive art experience. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

"What games should I play?"

**What the system returned:**

"You should try playing games like Wars, and Spelunky." — citing doc 08 as the source.

**Root cause (tied to a specific pipeline stage):**

This is primarily a grounding failure. Additionally, all six retrieved chunks had a high distance scores, indicating weak semantic matches and none of them actually address the question. The distance filter threshold of 0.55 was not tight enough to discard these chunks though; so they were passed to the LLM as context. The LLM latched onto a mid-sentence fragment "Wars, and Spelunky" from doc 08, which in its original context was part of a sentence recommending simple art styles, not games to play; and constructed a confident but misleading answer from it rather than recognizing the context was insufficient. Additionally, the question is out of scope for the system's purpose as an indie dev guide, and the LLM should have declined to answer it entirely.

**What you would change to fix it:**

First, updating the system prompt to include a stricter domain scope, explicitly instructing the LLM to decline questions unrelated to indie game development for artists. Additionally, tightening the distance filter threshold from 0.55 to around 0.45 so that weak matches are discarded before reaching the LLM, triggering the "not enough information" fallback without calling the LLM at all.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The evaluation questions in planning.md were immediately useful; where having 5 specific testable questions ready from the start meant retrieval could be tested against real expected answers rather than vague impressions. This made it easy to spot gaps early, like the engine recommendation question exposing that doc 01's Godot content wasn't surfacing reliably. The pre-planned chunking parameters (1000 characters, 200-character overlap) also served as a useful baseline to compare against; seeing concretely how the initial assumptions performed versus the final 300-character paragraph-aware approach gave a clear picture of how chunk size affects embedding signal. Additionally, having the spec and the Tinker Lab example as reference when prompting AI tools to generate code was valuable. Being able to share the chunking strategy section, architecture diagram, and retrieval approach directly in prompts produced more accurate and relevant code than starting from scratch.

**One way your implementation diverged from the spec, and why:**

The chunking strategy diverged significantly from the spec. The original plan specified 1000-character chunks with 200-character overlap, based on the assumption that long-form documents needed large chunks to preserve context. Testing revealed the opposite, where large chunks diluted the embedding signal by mixing multiple topics; and smaller paragraph-aware chunks at 300 characters with 20-character overlap produced more precise retrieval. The spec was updated to reflect the final implementation, but the divergence highlighted that chunking decisions can't be made confidently before seeing how the actual documents embed and retrieve.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*

The Chunking Strategy and Retrieval Approach sections from planning.md, the architecture diagram, and the Tinker Lab `ingest.py` and `retriever.py` as reference examples. I asked Claude to adapt these into a working ingestion and retrieval pipeline for my domain.

- *What it produced:*

A `ingest.py` with a character-based sliding window chunker at 1000 characters and 200-character overlap, and a `retriever.py` using `all-MiniLM-L6-v2` with ChromaDB — closely matching the lab structure but with the metadata key renamed from `"game"` to `"source"` and the collection name updated to `"indiedev_guide"`.

- *What I changed or overrode:*

The chunk size was iteratively reduced through testing (from 1000 to 600 to 300 characters) after observing that large chunks diluted the embedding signal and returned loosely related content (overlap and top-k chunks were also edited for similar reasons). The chunking strategy was also changed from a sliding window to a paragraph-aware grouping approach after mid-sentence chunk starts were identified as a retrieval quality issue.

**Instance 2**

- *What I gave the AI:*

The full planning.md, the Tinker Lab `generator.py` as a reference (with the lab grounding requirements). Then I asked Claude to adapt these into a working generator and grounding pipeline for my domain as a template to start with.

- *What it produced:*

A `generator.py` using Groq's `llama-3.3-70b-versatile` with a system prompt instructing the model to answer only from provided chunks, return a `SOURCES_USED:` line at the end, and say "I don't have enough information" when chunks are insufficient. It also returned a `handle_query` function and a Gradio UI wiring everything together.

- *What I changed or overrode:*

Along with some UI changes for clarity, the system prompt was tightened through several iterations: adding an explicit instruction not to list sources when refusing to answer, loosening the grounding instruction to allow synthesis across multiple chunks rather than requiring a single chunk to contain the full answer, and adding a distance filter of 0.55 to discard weak matches before they reached the LLM. The `SOURCES_USED:` parsing was also refined to correctly split the answer from the source list.
