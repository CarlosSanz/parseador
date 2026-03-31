# RFP Semantic Pipeline (Local, Zero-Cost First Iteration)

Proyecto local en Python para analizar RFPs y generar:

- `presentation_index.json`
- `working_enriched_index.json`
- `jvs_literal.json`
- `jvs_enriched.json`
- `traceability_matrix.csv`
- `quality_report.json`

## Stack
- FastAPI + Uvicorn
- Streamlit
- SQLite
- PyMuPDF (+ fallback pdfplumber)
- sentence-transformers
- FAISS

## Estructura
```text
rfp_semantic_pipeline/
├── app/
├── config/
├── data/
├── tests/
├── scripts/
├── requirements.txt
└── .env.example
```

## Configuración por entorno
1. Copia variables:
```bash
cp .env.example .env
```
2. Ajusta valores (LM Studio endpoint/modelo, rutas, etc.).

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar API
```bash
./scripts/run_api.sh
```

## Ejecutar UI Streamlit
```bash
./scripts/run_ui.sh
```

## Flujo funcional
1. Crear workspace.
2. Subir PDFs.
3. Ejecutar pipeline.
4. Revisar/descargar artefactos en `data/outputs/<workspace_id>/`.

## Notas de diseño
- Separación entre extracción literal y enriquecimiento semántico.
- Persistencia de salidas intermedias en `data/intermediate/`.
- Sin dependencias cloud obligatorias.
- Preparado para evolucionar a modelos/DB/infra cloud más adelante.
