from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "rfp_semantic_pipeline"
    app_env: str = "local"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    streamlit_port: int = 8501

    data_dir: Path = Field(default=Path("./data"))
    sqlite_path: Path = Field(default=Path("./data/rfp_pipeline.db"))
    taxonomy_path: Path = Field(default=Path("./config/taxonomy.yaml"))

    llm_provider: str = "lmstudio"
    llm_base_url: str = "http://localhost:1234/v1"
    llm_model: str = "gpt-oss-20b"
    llm_api_key: str = "lm-studio"

    embedding_provider: str = "local_sentence_transformer"
    embedding_model: str = "intfloat/multilingual-e5-large"
    embedding_dim: int = 1024
    faiss_index_path: Path = Field(default=Path("./data/vectorstores/chunks.faiss"))

    max_chunk_chars: int = 1200
    chunk_overlap_chars: int = 200

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def resolve_path(self, value: Path) -> Path:
        return value if value.is_absolute() else (self.project_root / value).resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir = settings.resolve_path(settings.data_dir)
    settings.sqlite_path = settings.resolve_path(settings.sqlite_path)
    settings.taxonomy_path = settings.resolve_path(settings.taxonomy_path)
    settings.faiss_index_path = settings.resolve_path(settings.faiss_index_path)
    return settings
