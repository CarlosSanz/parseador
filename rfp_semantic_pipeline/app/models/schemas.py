from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Document(BaseModel):
    document_id: str
    filename: str
    document_type: str
    language: str
    sha256: str
    upload_timestamp: datetime
    workspace_id: str


class PageBlock(BaseModel):
    page_num: int
    text: str
    source_file: str


class Section(BaseModel):
    section_id: str
    section_code: str
    section_title: str
    page_start: int
    page_end: int
    parent_section_id: str | None = None


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    section_id: str | None = None
    text: str
    chunk_type: str = "section_chunk"
    semantic_labels: list[str] = Field(default_factory=list)
    scope: str = "global"
    pilot_ids: list[str] = Field(default_factory=list)
    candidate_index_enrichment: bool = False
    candidate_jv_support: bool = False


class Pilot(BaseModel):
    pilot_id: str
    title: str
    description: str
    source_reference: str


class IndexNode(BaseModel):
    node_id: str
    code: str
    title_literal: str
    title_working: str
    level: int
    mandatory: bool
    origin: str
    source_references: list[str] = Field(default_factory=list)
    linked_jv_ids: list[str] = Field(default_factory=list)


class JVItem(BaseModel):
    jv_id: str
    parent_jv_id: str | None = None
    title: str
    literal_text: str
    points: float | None = None
    application_scope: str = "global"
    primary_index_owner: str | None = None
    linked_ppt_sections: list[str] = Field(default_factory=list)
    what_is_evaluated: str | None = None
    response_must_include: list[str] = Field(default_factory=list)


class TraceabilityRow(BaseModel):
    jv_id: str
    index_node_id: str
    support_chunk_ids: list[str]
    coverage_type: Literal["full", "partial", "weak"]
    confidence: float


class QualityReport(BaseModel):
    jvs_without_owner: list[str] = Field(default_factory=list)
    owners_without_support: list[str] = Field(default_factory=list)
    low_confidence_nodes: list[str] = Field(default_factory=list)
    possible_duplicates: list[str] = Field(default_factory=list)
    terminology_inconsistencies: list[str] = Field(default_factory=list)
