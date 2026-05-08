def chunk_text(
    text: str,
    chunk_size: int = 3000,
    overlap: int = 400,
) -> list[str]:

    if not text or not text.strip():
        return []

    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = ' '.join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start += chunk_size - overlap

    return chunks
    