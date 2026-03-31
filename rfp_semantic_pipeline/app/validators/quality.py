from app.models.schemas import IndexNode, JVItem, QualityReport, TraceabilityRow


def build_quality_report(jvs: list[JVItem], nodes: list[IndexNode], rows: list[TraceabilityRow]) -> QualityReport:
    jvs_without_owner = [jv.jv_id for jv in jvs if not jv.primary_index_owner]
    node_ids = {node.node_id for node in nodes}
    owners_without_support = [jv.primary_index_owner for jv in jvs if jv.primary_index_owner and jv.primary_index_owner not in node_ids]
    low_conf = [row.index_node_id for row in rows if row.confidence < 0.6]
    return QualityReport(
        jvs_without_owner=jvs_without_owner,
        owners_without_support=list(set(owners_without_support)),
        low_confidence_nodes=low_conf,
        possible_duplicates=[],
        terminology_inconsistencies=[],
    )
