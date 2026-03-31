from app.models.schemas import Chunk, Document, PageBlock, Section


class SemanticChunker:
    def __init__(self, max_chars: int = 1200, overlap: int = 200) -> None:
        self.max_chars = max_chars
        self.overlap = overlap

    def create_chunks(self, document: Document, pages: list[PageBlock], sections: list[Section]) -> list[Chunk]:
        all_text = "\n".join(p.text for p in pages)
        if not all_text:
            return []
        chunks: list[Chunk] = []
        start = 0
        index = 1
        while start < len(all_text):
            end = min(start + self.max_chars, len(all_text))
            text = all_text[start:end]
            section_id = sections[0].section_id if sections else None
            chunks.append(
                Chunk(
                    chunk_id=f"{document.document_id}_chunk_{index}",
                    document_id=document.document_id,
                    section_id=section_id,
                    text=text,
                )
            )
            start = end - self.overlap
            index += 1
            if start < 0:
                start = 0
            if end == len(all_text):
                break
        return chunks
