from app.models.schemas import IndexNode, JVItem, TraceabilityRow
from app.validators.quality import build_quality_report


def test_quality_report_detects_missing_owner():
    jvs = [JVItem(jv_id="j1", title="x", literal_text="y")]
    nodes = [
        IndexNode(
            node_id="idx_1",
            code="1",
            title_literal="a",
            title_working="a",
            level=1,
            mandatory=True,
            origin="x",
        )
    ]
    rows = [TraceabilityRow(jv_id="j1", index_node_id="idx_1", support_chunk_ids=[], coverage_type="partial", confidence=0.9)]

    report = build_quality_report(jvs, nodes, rows)
    assert report.jvs_without_owner == ["j1"]
