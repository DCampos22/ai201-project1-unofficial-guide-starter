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

This system covers CS courses, professors, and degree requirements at Queens College, CUNY. The knowledge is valuable because it's scattered across unofficial forums, rating sites, and buried catalog pages that students have to piece together on their own. Official channels (the QC catalog, department website) tell you what courses exist but not which professors are worth taking, which courses are hardest, or how to realistically plan your schedule. Student reviews on Reddit and Rate My Professors fill that gap but aren't searchable in one place.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors – QC CS | Web (professor reviews) | https://www.ratemyprofessors.com/search/professors/231?q=*&did=11 |
| 2 | Reddit – CS professors thread | Forum thread | https://www.reddit.com/r/QueensCollege/comments/rm2wqi/cs_professors/ | Forum thread | https://www.reddit.com/r/QueensCollege/comments/1mlcmk1/comp_sci_at_queens/ |
| 4 | QC Catalog – CS Faculty | Official catalog page | https://qc-undergraduate.catalog.cuny.edu/departments/CSCI-QC/faculty |
| 5 | QC CS Dept – Full-time faculty | Department website | https://www.cs.qc.cuny.edu/fulltime.php |
| 6 | QC Catalog – CS Courses | Official catalog page | https://qc-undergraduate.catalog.cuny.edu/departments/CSCI-QC/courses |
| 7 | r/CUNY subreddit | Forum | https://www.reddit.com/r/CUNY/ |
| 8 | QC Catalog – CS BA Program | Official catalog page | https://qc-undergraduate.catalog.cuny.edu/programs/CSCI-BA |
| 9 |QC Catalog – CS BS Program | Official catalog page  Official catalog page | https://qc-undergraduate.catalog.cuny.edu/programs/CSCI-BS |
| 10 | Insider student notes | Local File |  documents/Student_Experience.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 150 words

**Overlap:** 30 words

**Why these choices fit your documents:** RMP reviews are short (2–5 sentences), Reddit threads are conversational paragraphs, and catalog pages are dense structured text. A 150-word chunk is large enough to capture a complete review or a meaningful paragraph without cutting off mid-thought, while small enough that each chunk stays focused on one topic. Chunks smaller than ~30 words risk splitting a single review in half, losing context.
Chunks larger than ~300 words lump multiple professors' reviews together, making retrieval noisy. The 30-word overlap ensures that key facts sitting at chunk boundaries
(like a course number or professor name) appear in at least one complete chunk. A minimum length filter of 30 words was also applied to drop footer fragments and boilerplate that survived cleaning.

**Final chunk count:** 69 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)


**Production tradeoff reflection:** all-MiniLM-L6-v2 is lightweight and fast, running locally with no rate limits or cost, ideal for a student project. It maps semantically similar text close together in vector space, so a query like "which professor is good for data structures" can retrieve a chunk mentioning CS 320 even without exact word overlap. In a real deployment, I'd consider OpenAI's text-embedding-3-large for better accuracy on domain-specific academic language, or a multilingual model given QC's diverse student population. The tradeoff would be higher latency and API cost versus marginal accuracy gains for this relatively straightforward domain. Context length would also matter more if documents were longer, all-MiniLM-L6-v2 has a 256-token limit which is fine for reviews but would truncate longer guides.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are a helpful guide for Computer Science students at Queens College, CUNY.

Answer questions using ONLY the information provided in the context below.

If the context does not contain enough information to answer the question, say exactly:

"I don't have enough information on that in my documents."

Do not use any outside knowledge. Always cite which source document your answer comes from.

**How source attribution is surfaced in the response:**
Source attribution is handled two ways. First, the system prompt instructs the LLM to cite source documents inline in its response. Second, the retrieved source filenames are
collected programmatically from ChromaDB metadata and displayed in a separate "Retrieved from" field in the Gradio UI, independent of what the LLM writes. This means attribution is guaranteed even if the model forgets to cite inline.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What courses are required for the CS BA degree? | CS 111, 211, 220, 320, 323, 331, 340 + math | Listed EC1/EC2, MATH 151/152, CSCI 111, 211, 212, 313, 320, 343, MATH 241, 231/237 with source citations | Relevant | Accurate |
| 2 | What is the difference between CS BA and CS BS? | BS requires more math/science; BA is more flexible | Correctly identified BA has 66/67 major credits + 12/11 elective vs BS 78/79 major + 0 elective; noted course sequencing differs | Relevant | Partially accurate |
| 3 | What is the prerequisite for CS 320? | CS211 | "I don't have enough information on that in my documents." | Off-target | Inaccurate |
| 4 | What do Reddit users recommend for surviving the CS program? | Office hours, study groups, starting early | "I don't have enough information on that in my documents." | Off-target | Inaccurate |
| 5 | How many credits is the CS BA program? | 120 credits | Correctly summed credit categories, concluded 120 or 121 depending on track, cited source | Relevant | Accurate |

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
"What is the prerequisite for CS 320 at Queens College?"

**What the system returned:**
"I don't have enough information on that in my documents."

**Root cause (tied to a specific pipeline stage):**
This is a chunking and document structure issue. The course catalog page (qc_catalog_courses.txt) lists courses in a dense flat format — course code, title, credits, and designation, but does not include prerequisite information inline. The prerequisite for CS 320 (CS 211) appears in a separate section of the catalog that was either not captured during manual copy-paste or got split across chunk boundaries such that no single chunk contains both "CSCI 320" and "prerequisite." The retrieval This is a chunking and document structure issue. The course catalog page (qc_catalog_courses.txt) lists courses in a dense flat format, course code, title, credits, and designation, but does not include prerequisite information inline. The prerequisite for CS 320 (CS 211) appears in a separate section of the catalog that was either not captured during manual copy-paste or got split across chunk boundaries such that no single chunk contains both "CSCI 320" and "prerequisite." The retrieval stage returned catalog chunks correctly but none of them contained the prerequisite detail, so the LLM correctly declined to answer rather than hallucinate.

**What you would change to fix it:**
Re-collect the course catalog document to include the full course description pages, which list prerequisites explicitly. Alternatively, scrape individual course detail
pages rather than the course listing overview page, which only has high-level metadata.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The Chunking Strategy section of planning.md directly shaped debugging decisions. When the initial chunk count came back at 33 (too low), I had a written spec to compare
against the plan called for 150-word chunks, but the implementation was using 350, which was too large for the short review documents. Having the spec written down made
it easy to identify the mismatch and fix it rather than guessing.

**One way your implementation diverged from the spec, and why:**
The spec called for tiktoken for token counting, but the implementation ended up using word-based splitting instead. This was a practical decision, tiktoken requires an additional install and the token-to-word ratio for this corpus is close enough to 1:1 that word count is a reasonable proxy. The chunk sizes in the spec (300–400 tokens) were also revised down to 150 words during implementation after seeing that 350-word chunks produced only 33 total chunks, not enough coverage for the corpus size.

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

- *What I gave the AI:* The Documents section and Chunking Strategy section from planning.md, plus a request to implement `load_documents()` and `chunk_text()`
- *What it produced:* A working script that loaded .txt files with metadata and split by word count with overlap
- *What I changed or overrode:* Chunk size was reduced from 350 to 150 words after seeing that 350 produced only 33 chunks — too few for meaningful retrieval. A minimum 30-word filter was also added to drop footer fragments that survived cleaning.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section and the full pipeline context, with a request to implement embedding, ChromaDB storage, and a Gradio interface
- *What it produced:* `retrieve.py` with `build_vector_store()` and `retrieve()`, and `app.py` with a Groq-powered generation function and Gradio UI
- *What I changed or overrode:* The original generation code used the OpenAI API as planned in the spec, but was switched to Groq's llama-3.3-70b-versatile because it's free-tier with no credit card required. The grounding instruction was also tightened to include an exact fallback phrase ("I don't have enough information on that in my documents") so the model's decline behavior would be consistent and testable.
