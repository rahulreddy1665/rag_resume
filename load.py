from pypdf import PdfReader
def load_resume(path):
    reader = PdfReader(path)
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return "\n".join(pages_text)
if __name__ == "__main__":
    text = load_resume("resume.pdf")
    print(text)
    print("-" * 40)
    print("Characters:", len(text))
    print("Words:", len(text.split()))