# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This domain covers CS courses and professors at Queens College, CUNY including student reviews, degree requirements, and course expectations. This knowledge is valuable because it's scattered across unofficial forums, rating sites, and buried catalog pages that students have to piece together on their own. There's no single place a new QC CS student can go to understand which professors to take, which courses are hardest, or how to plan their schedule.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors - QC CS | All CS professor listings and reviews | https://www.ratemyprofessors.com/search/professors/231?q=*&did=11 |
| 2 | Reddit thread – CS professors | Reddit thread – CS professors | https://www.reddit.com/r/QueensCollege/comments/rm2wqi/cs_professors/ |
| 3 | Reddit thread – Comp Sci at QC | General experience with the CS program | https://www.reddit.com/r/QueensCollege/comments/1mlcmk1/comp_sci_at_queens/ |
| 4 | QC Catalog – CS Faculty | QC Catalog – CS Faculty | https://qc-undergraduate.catalog.cuny.edu/departments/CSCI-QC/faculty |
| 5 | QC CS Dept – Full-time faculty | Faculty contact and research info | https://www.cs.qc.cuny.edu/fulltime.php |
| 6 | QC Catalog – CS Courses | Full course descriptions and prereqs | https://qc-undergraduate.catalog.cuny.edu/departments/CSCI-QC/courses |
| 7 | r/CUNY subreddit | Broader CUNY CS student discussions | https://www.reddit.com/r/CUNY/ |
| 8 | QC Catalog – CS BA Program | Degree requirements for CS BA | https://qc-undergraduate.catalog.cuny.edu/programs/CSCI-BA |
| 9 | QC Catalog - CS BS Program | Degree requirements for CS BS | https://qc-undergraduate.catalog.cuny.edu/programs/CSCI-BS |
| 10 | Insider student notes | Previous student experience | C:\Users\damar\OneDrive\Desktop\CodePath\New folder\ai201-project1-unofficial-guide-starter\Student_Experience.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300-400 tokens 

**Overlap:** 50 tokens

**Reasoning:** My corpus is mixed where RMP reviews are short (2–5 sentences), Reddit threads are conversational paragraphs, and catalog pages are dense structured text. A 300–400 token chunk is large enough to capture a complete review or a meaningful paragraph from a longer guide without cutting off mid-thought. Chunks smaller than ~200 tokens risk splitting a single review in half, losing context (e.g. "Great professor" separated from "but the exams are brutal"). Chunks larger than ~500 tokens would 
lump multiple professors' reviews together, making retrieval noisy. The 50-token overlap handles the case where a key fact (like a course number or 
professor name) sits at the boundary between two chunks — overlap ensures at least one chunk contains the full sentence. Without overlap, a query about "CS 320 
difficulty" could fail if that sentence was split across chunk boundaries.

Too-small chunks would cause retrieval failures on multi-sentence opinions. Too-large chunks would return irrelevant content mixed in with relevant content, 
making the LLM's job harder.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5 chuncks per query

**Production tradeoff reflection:** 
all-MiniLM-L6-v2 is a lightweight, fast model that works well for short to medium-length opinion text, which matches most of my corpus (reviews, Reddit posts). It maps semantically similar text close together in vector space, so a query like "which professor is good for data structures" can retrieve a chunk that says "Professor X makes CS320 very approachable" even without exact word overlap.

Top-k of 5 gives the LLM enough context to synthesize across multiple reviews or sources without flooding it with irrelevant content. Too few (k=1 or 2) risks missing relevant chunks if the top result is slightly off. Too many (k=10+) risks pulling in unrelated professors or courses and confusing the response.

If cost weren't a constraint, I'd consider OpenAI's text-embedding-3-large for better accuracy on domain-specific academic language, or a multilingual model if serving non-English-speaking QC students. The tradeoff would be higher latency and API cost vs. the marginal accuracy gain for this relatively simple domain.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What courses are required for the CS BA degree at Queens College? | CS 111, 112, 211, 220, 320, 323, 331, 340, plus math requirements including Calculus and Discrete Math (verifiable from catalog) |
| 2 | What is the difference between the CS BA and CS BS degree at Queens College? | The BS requires additional math/science courses including Physics and more advanced math electives; the BA is more flexible (verifiable from both catalog program pages) |
| 3 | What is the prerequisite for CS 320 at Queens College? | CS 211 (verifiable from course catalog) |
| 4 | What do Reddit users recommend for surviving the CS program at QC? | Responses should include advice like starting early, going to office hours, forming study groups — verifiable from Reddit threads |
| 5 | How many credits is the CS BA program at Queens College? | 120 credits total (verifiable from degree requirements page) |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **RMP and Reddit content is noisy and inconsistent.**
Reviews vary wildly in length, specificity, and tone. Some are one sentence ("great prof!"), others are detailed paragraphs. This inconsistency makes chunking harder, a fixed token size might split a detailed review mid-sentence while leaving a one-liner as its own tiny chunk that lacks enough context to be useful on its own.

2. **Catalog pages for BA and BS programs overlap significantly in content.** 
The BA and BS degree pages share many of the same required courses, so chunks from both pages may be retrieved for the same query. This could cause the system to conflate the two programs and give a student incorrect advice about which requirements apply to them. Metadata tagging by source URL would help distinguish BA vs BS chunks at retrieval time.


---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     ```
Document Ingestion        Chunking              Embedding + Vector Store
──────────────────   →   ──────────────────   →   ──────────────────────────
Local .txt files          350 tokens /             sentence-transformers
RMP, Reddit, Catalog      50 token overlap         (all-MiniLM-L6-v2)
(scraped + saved)         tiktoken                 ChromaDB

        ↓
   Retrieval                          Generation
──────────────────────────   →   ──────────────────────────
ChromaDB similarity search         OpenAI API (gpt-3.5-turbo)
top-k = 5 chunks                   chunks passed as context
                                   natural language response
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Stage 1 — Document ingestion:**
I'll give Claude the list of 10 sources from the Documents section above and ask it 
to write a `load_documents()` function that reads from local `.txt` files and returns 
a list of document strings with metadata (source name, URL).

**Stage 2 — Chunking:**
I'll give Claude the Chunking Strategy section of this planning.md and ask it to 
implement a `chunk_text()` function using a 350-token chunk size with 50-token 
overlap. I'll specify that it should use the `tiktoken` library for token counting.

**Stage 3 — Embedding + vector store:**
I'll give Claude the Retrieval Approach section and ask it to implement 
`embed_and_store()` using sentence-transformers (all-MiniLM-L6-v2) and ChromaDB as 
the vector store.

**Stage 4 — Retrieval:**
I'll give Claude the retrieval section and ask it to implement a `retrieve()` function 
that takes a query string and returns the top 5 most relevant chunks from ChromaDB.

**Stage 5 — Generation:**
I'll give Claude the full pipeline context and ask it to implement the final 
`generate_response()` function that takes retrieved chunks, formats them as context, 
and calls the OpenAI API to produce an answer.

---

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
