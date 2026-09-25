import pymupdf


def extract_pages(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()

        pdf = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()

            if text:
                documents.append({
                    "text": text,
                    "source": uploaded_file.name,
                    "page": page_number
                })

        pdf.close()

    return documents


def create_chunks(documents, chunk_size=1000, overlap=150):
    chunks = []

    for document in documents:
        text = document["text"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"]
                })

            start += chunk_size - overlap

    return chunks