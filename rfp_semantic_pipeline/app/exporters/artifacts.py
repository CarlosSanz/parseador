from pathlib import Path

from app.core.files import dump_json
from app.models.schemas import IndexNode, JVItem, QualityReport


def export_json_artifacts(
    output_dir: Path,
    presentation_index: list[IndexNode],
    working_index: list[IndexNode],
    jvs_literal: list[JVItem],
    jvs_enriched: list[JVItem],
    quality_report: QualityReport,
) -> None:
    dump_json(output_dir / "presentation_index.json", [n.model_dump() for n in presentation_index])
    dump_json(output_dir / "working_enriched_index.json", [n.model_dump() for n in working_index])
    dump_json(output_dir / "jvs_literal.json", [j.model_dump() for j in jvs_literal])
    dump_json(output_dir / "jvs_enriched.json", [j.model_dump() for j in jvs_enriched])
    dump_json(output_dir / "quality_report.json", quality_report.model_dump())
