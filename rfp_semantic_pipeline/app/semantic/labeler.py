from app.models.schemas import Chunk


KEYWORDS = {
    "ARCHITECTURE": ["arquitectura", "architecture"],
    "SECURITY": ["seguridad", "security", "ciber"],
    "TRACEABILITY": ["trazabilidad", "traceability"],
    "DATA_ANALYSIS": ["análisis", "analysis", "analit"],
    "DELIVERABLE": ["entregable", "deliverable"],
}


class SemanticLabeler:
    def __init__(self, taxonomy: list[str]) -> None:
        self.taxonomy = taxonomy

    def label_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        for chunk in chunks:
            lowered = chunk.text.lower()
            labels = [label for label, kws in KEYWORDS.items() if any(k in lowered for k in kws)]
            if not labels:
                labels = ["GENERAL_APPROACH"]
            chunk.semantic_labels = [label for label in labels if label in self.taxonomy]
            chunk.candidate_index_enrichment = any(l in {"DELIVERABLE", "ARCHITECTURE"} for l in chunk.semantic_labels)
            chunk.candidate_jv_support = any(l in {"TRACEABILITY", "SECURITY", "DATA_ANALYSIS"} for l in chunk.semantic_labels)
        return chunks
