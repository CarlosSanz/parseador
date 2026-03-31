import csv
from pathlib import Path

from app.models.schemas import Chunk, IndexNode, JVItem, TraceabilityRow


def build_traceability(jvs: list[JVItem], nodes: list[IndexNode], chunks: list[Chunk]) -> list[TraceabilityRow]:
    rows: list[TraceabilityRow] = []
    support_ids = [c.chunk_id for c in chunks[:3]]
    node_id = nodes[0].node_id if nodes else "idx_1"
    for jv in jvs:
        rows.append(
            TraceabilityRow(
                jv_id=jv.jv_id,
                index_node_id=node_id,
                support_chunk_ids=support_ids,
                coverage_type="partial",
                confidence=0.7,
            )
        )
    return rows


def export_traceability_csv(rows: list[TraceabilityRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["jv_id", "index_node_id", "support_chunk_ids", "coverage_type", "confidence"])
        for row in rows:
            writer.writerow([row.jv_id, row.index_node_id, "|".join(row.support_chunk_ids), row.coverage_type, row.confidence])
