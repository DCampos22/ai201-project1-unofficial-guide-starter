import os
import re

DOCUMENTS_DIR = "documents"

def load_documents():
    documents = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt") and filename != ".gitkeep":
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            cleaned = clean_text(raw_text)
            if cleaned.strip():
                documents.append({
                    "source": filename,
                    "text": cleaned
                })
    return documents


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove HTML entities
    text = re.sub(r"&[a-z]+;", " ", text)
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Remove catalog header
    text = re.sub(r"Catalog Home Page.*?Download as PDF", "", text)
    # Remove promoted ad blocks
    text = re.sub(r"•\s*Promoted.*?(?=\n\n|\d+[yo] ago|Comments Section)", "", text, flags=re.DOTALL)
    # Remove leftover navigation remnants
    text = re.sub(r"Open menu Find anything Ask Find anything", "", text)
    text = re.sub(r"Comp Sci at Queens : ", "", text)
    text = re.sub(r"CS Professors : ", "", text)
    # Remove common nav/footer boilerplate
    boilerplate = [
        "Skip to Main Content",
        "Skip to main content",
        "About QCAdmissionsAcademicsStudent LifeCommunity OutreachMake A Gift",
        "Reddit Rules Privacy Policy User Agreement",
        "Reddit, Inc.",
        "All rights reserved",
        "Expand user menu",
        "Open menu Find anything",
        "Go to QueensCollege",
        "Log In",
        "Accessibility",
        "Clickable image which will reveal the video player",
        "Learn More",
        "r/QueensCollege",
        "Thumbnail image:",
        "atlassian.com",
        "nike.com",
        "shop.off.com",
        "Shop Now",
        "Catalog Home Page Download as PDF",
        "Collapse video player",
        "0:00 / 0:00",
    ]
    for phrase in boilerplate:
        text = text.replace(phrase, "")
    # Remove copyright lines and avatar lines
    text = re.sub(r"Catalog Home Page\s*\n+\s*Download as PDF", "", text)
    text = re.sub(r"(•\s*Promoted|Promoted).*?(?=Comments Section|\d+[yo] ago|$)", "", text, flags=re.DOTALL)
    text = re.sub(r"©\s*\d{4}.*", "", text)
    text = re.sub(r"u/\w+\s+avatar\s+\w+.*", "", text)
    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=150, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks


def main():
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents\n")

    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            if len(chunk.split()) > 30:
                all_chunks.append({
                    "source": doc["source"],
                    "chunk": chunk
                })

    print(f"Total chunks: {len(all_chunks)}\n")

    print("--- 5 SAMPLE CHUNKS ---\n")
    for i in [0, 10, 20, 30, 40]:
        if i < len(all_chunks):
            print(f"[{all_chunks[i]['source']}]")
            print(all_chunks[i]['chunk'])
            print("---")

if __name__ == "__main__":
    main()