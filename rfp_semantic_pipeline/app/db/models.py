from datetime import datetime

from sqlmodel import Field, SQLModel


class WorkspaceRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    workspace_id: str = Field(index=True)
    filename: str
    document_type: str
    language: str
    sha256: str
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    path: str


class ChunkRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    workspace_id: str = Field(index=True)
    document_id: str = Field(index=True)
    section_id: str | None = None
    text: str
    semantic_labels: str = "[]"
