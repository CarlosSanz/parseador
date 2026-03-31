from pathlib import Path

import pandas as pd
import streamlit as st

from app.core.pipeline import PipelineService


st.set_page_config(page_title="RFP Semantic Pipeline", layout="wide")
st.title("RFP Semantic Pipeline (Local)")

service = PipelineService()

if "workspace_id" not in st.session_state:
    st.session_state.workspace_id = None

st.header("1) Home")
if st.button("Crear workspace"):
    st.session_state.workspace_id = service.create_workspace()
    st.success(f"Workspace creado: {st.session_state.workspace_id}")

st.header("2) Upload")
uploaded_files = st.file_uploader("Sube PDFs de la RFP", type=["pdf"], accept_multiple_files=True)

st.header("3) Run Pipeline")
if st.button("Ejecutar pipeline"):
    if not st.session_state.workspace_id:
        st.error("Primero crea un workspace.")
    elif not uploaded_files:
        st.error("Sube al menos un PDF.")
    else:
        payload = [(f.name, f.getvalue()) for f in uploaded_files]
        docs = service.ingest_files(st.session_state.workspace_id, payload)
        result = service.run(st.session_state.workspace_id, docs)
        st.session_state.result = result
        st.success("Pipeline ejecutado")
        st.json(result)

st.header("4) Results")
result = st.session_state.get("result")
if result:
    output_dir = Path(result["output_dir"])
    st.write("Artefactos:", result["artifacts"])
    for artifact in result["artifacts"]:
        file_path = output_dir / artifact
        if artifact.endswith(".json"):
            st.subheader(artifact)
            st.json(file_path.read_text(encoding="utf-8"))
        elif artifact.endswith(".csv"):
            st.subheader(artifact)
            st.dataframe(pd.read_csv(file_path))
        with st.expander(f"Descargar {artifact}"):
            st.download_button(
                label=f"Descargar {artifact}",
                data=file_path.read_bytes(),
                file_name=artifact,
                mime="application/octet-stream",
            )
