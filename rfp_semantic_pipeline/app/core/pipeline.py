from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from app.chunking.chunker import SemanticChunker
from app.core.files import compute_sha256, dump_json, ensure_dirs, load_taxonomy
from app.core.settings import get_settings
from app.embeddings.service import EmbeddingService, FaissStore
from app.enrichment.enricher import enrich_index, enrich_jvs
from app.exporters.artifacts import export_json_artifacts
from app.extraction.jvs import extract_jvs_literal
from app.extraction.presentation_index import extract_presentation_index
from app.models.schemas import Document
from app.parsers.pdf_parser import PDFParser
from app.semantic.labeler import SemanticLabeler
from app.traceability.matrix import build_traceability, export_traceability_csv
from app.validators.quality import build_quality_report


class PipelineService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.parser = PDFParser()
        self.chunker = SemanticChunker(self.settings.max_chunk_chars, self.settings.chunk_overlap_chars)
        self.taxonomy = load_taxonomy(self.settings.taxonomy_path)
        self.labeler = SemanticLabeler(self.taxonomy)
        self.embedding_service = EmbeddingService(self.settings.embedding_model, self.settings.embedding_dim)
        self.faiss_store = FaissStore(self.settings.embedding_dim, self.settings.faiss_index_path)

    def create_workspace(self) -> str:
        workspace_id = f"ws_{uuid.uuid4().hex[:10]}"
        ensure_dirs([
            self.settings.data_dir / "workspaces" / workspace_id,
            self.settings.data_dir / "outputs" / workspace_id,
            self.settings.data_dir / "intermediate" / workspace_id,
        ])
        return workspace_id

    def ingest_files(self, workspace_id: str, files: list[tuple[str, bytes]]) -> list[Document]:
        docs: list[Document] = []
        base = self.settings.data_dir / "workspaces" / workspace_id
        for filename, content in files:
            target = base / filename
            target.write_bytes(content)
            docs.append(
                Document(
                    document_id=f"doc_{uuid.uuid4().hex[:8]}",
                    filename=filename,
                    document_type=self._detect_type(filename),
                    language="unknown",
                    sha256=compute_sha256(content),
                    upload_timestamp=datetime.utcnow(),
                    workspace_id=workspace_id,
                )
            )
        return docs

    def run(self, workspace_id: str, documents: list[Document]) -> dict:
        all_chunks = []
        output_dir = self.settings.data_dir / "outputs" / workspace_id
        intermediate_dir = self.settings.data_dir / "intermediate" / workspace_id

        for document in documents:
            path = self.settings.data_dir / "workspaces" / workspace_id / document.filename
            pages = self.parser.parse_pages(path)
            sections = self.parser.detect_sections(pages)
            chunks = self.chunker.create_chunks(document, pages, sections)
            all_chunks.extend(chunks)

            dump_json(intermediate_dir / f"{document.document_id}_pages.json", [p.model_dump() for p in pages])
            dump_json(intermediate_dir / f"{document.document_id}_sections.json", [s.model_dump() for s in sections])

        labeled_chunks = self.labeler.label_chunks(all_chunks)
        vectors = self.embedding_service.embed_texts([c.text for c in labeled_chunks])
        self.faiss_store.add(vectors)
        self.faiss_store.save()

        presentation_index = extract_presentation_index(labeled_chunks)
        jvs_literal = extract_jvs_literal(labeled_chunks)
        working_index = enrich_index(presentation_index, labeled_chunks)
        jvs_enriched = enrich_jvs(jvs_literal, working_index, labeled_chunks)
        rows = build_traceability(jvs_enriched, working_index, labeled_chunks)
        quality = build_quality_report(jvs_enriched, working_index, rows)

        export_json_artifacts(output_dir, presentation_index, working_index, jvs_literal, jvs_enriched, quality)
        export_traceability_csv(rows, output_dir / "traceability_matrix.csv")
        dump_json(intermediate_dir / "chunks_enriched.json", [c.model_dump() for c in labeled_chunks])

        return {
            "workspace_id": workspace_id,
            "documents": [d.model_dump(mode="json") for d in documents],
            "chunks": len(labeled_chunks),
            "output_dir": str(output_dir),
            "artifacts": sorted(p.name for p in output_dir.glob("*")),
        }

    def _detect_type(self, filename: str) -> str:
        lowered = filename.lower()
        if "pcap" in lowered or "administr" in lowered:
            return "administrative"
        if "ppt" in lowered or "tecn" in lowered or "technic" in lowered:
            return "technical"
        return "complementary"
