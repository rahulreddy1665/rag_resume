from load import load_resume
def chunk_text(text, chunk_size=120, overlap=30):
    text = text.replace("+91 7892380489", "")
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(words), step):
        end = start + chunk_size
        if len(words) - end < overlap:
            end = len(words)
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
    return chunks
SECTION_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "PROJECTS",
    "EDUCATION",
]
COMPANIES = ["JNET Technologies","Agilets Pvt Ltd", "Zevcore Pvt Ltd"]
def split_into_sections(text):
    sections = []
    section = "CONTACT"
    title = "CONTACT"
    lines = []
    for line in text.splitlines():
        clean = line.strip()
        is_heading = clean.upper() in SECTION_HEADINGS
        is_job = (section == "PROFESSIONAL EXPERIENCE"
                  and any(clean.startswith(c) for c in COMPANIES))
        if is_heading or is_job:
            if "Zevcore" in line:
                print(repr(line))
            if lines:
                sections.append((title, " ".join(lines)))
            if is_heading:
                section = clean.upper()
                title = section
            else:
                title = f"{section} – {clean}"
            lines = []
        elif clean:
            lines.append(clean)
    if lines:
        sections.append((title, " ".join(lines)))
    return sections

def chunk_by_section(text, max_words=150, overlap=30):
    chunks = []
    for title, body in split_into_sections(text):
        for piece in chunk_text(body, chunk_size=max_words, overlap=overlap):
            chunks.append(f"{title}: {piece}")
    return chunks
    
if __name__ == "__main__":
    text = load_resume("resume.pdf")
    for title, body in split_into_sections(text):
        print(f"{title}: {len(body.split())} words")

    chunks = chunk_by_section(text)
    print("\nTotal chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ---\n{chunk[:150]} ...")