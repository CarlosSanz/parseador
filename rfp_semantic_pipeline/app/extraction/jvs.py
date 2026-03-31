from app.models.schemas import Chunk, JVItem


def extract_jvs_literal(chunks: list[Chunk]) -> list[JVItem]:
    jvs: list[JVItem] = []
    j = 1
    for chunk in chunks:
        if chunk.candidate_jv_support:
            jvs.append(
                JVItem(
                    jv_id=f"jv_{j}",
                    title=f"Criterio JV {j}",
                    literal_text=chunk.text[:400],
                    points=10.0,
                )
            )
            j += 1
    if not jvs:
        jvs.append(JVItem(jv_id="jv_1", title="Criterio general", literal_text="No detectado automáticamente", points=0.0))
    return jvs
