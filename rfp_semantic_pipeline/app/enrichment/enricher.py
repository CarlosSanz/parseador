from app.models.schemas import Chunk, IndexNode, JVItem


def enrich_index(nodes: list[IndexNode], chunks: list[Chunk]) -> list[IndexNode]:
    for node in nodes:
        node.title_working = f"{node.title_literal} (enriched)"
        for chunk in chunks[:2]:
            if chunk.chunk_id not in node.source_references:
                node.source_references.append(chunk.chunk_id)
    return nodes


def enrich_jvs(jvs: list[JVItem], nodes: list[IndexNode], chunks: list[Chunk]) -> list[JVItem]:
    owner = nodes[0].node_id if nodes else None
    section = chunks[0].section_id if chunks else None
    for jv in jvs:
        jv.primary_index_owner = owner
        if section:
            jv.linked_ppt_sections = [section]
        jv.what_is_evaluated = "Capacidad técnica, trazabilidad y valor de la solución"
        jv.response_must_include = ["enfoque", "metodología", "evidencias"]
    return jvs
