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

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
