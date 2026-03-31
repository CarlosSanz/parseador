from app.models.schemas import Chunk, IndexNode


def extract_presentation_index(chunks: list[Chunk]) -> list[IndexNode]:
    nodes: list[IndexNode] = []
    for i, chunk in enumerate(chunks, start=1):
        if chunk.candidate_index_enrichment:
            nodes.append(
                IndexNode(
                    node_id=f"idx_{i}",
                    code=f"{i}",
                    title_literal=f"Apartado técnico {i}",
                    title_working=f"Apartado técnico {i}",
                    level=1,
                    mandatory=True,
                    origin="literal_extraction",
                    source_references=[chunk.chunk_id],
                )
            )
    if not nodes:
        nodes.append(
            IndexNode(
                node_id="idx_1",
                code="1",
                title_literal="Propuesta técnica",
                title_working="Propuesta técnica",
                level=1,
                mandatory=True,
                origin="fallback",
                source_references=[],
            )
        )
    return nodes
