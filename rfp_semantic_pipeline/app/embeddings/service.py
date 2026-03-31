from __future__ import annotations

import hashlib
from pathlib import Path

import faiss
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None


class EmbeddingService:
    def __init__(self, model_name: str, dim: int) -> None:
        self.model_name = model_name
        self.dim = dim
        self.model = SentenceTransformer(model_name) if SentenceTransformer else None

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype="float32")
        if self.model:
            vectors = self.model.encode(texts, normalize_embeddings=True)
            return np.array(vectors, dtype="float32")
        return np.array([self._fallback_embedding(t) for t in texts], dtype="float32")

    def _fallback_embedding(self, text: str) -> np.ndarray:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        repeated = (digest * ((self.dim // len(digest)) + 1))[: self.dim]
        arr = np.frombuffer(repeated, dtype=np.uint8).astype("float32")
        norm = np.linalg.norm(arr)
        return arr / norm if norm > 0 else arr


class FaissStore:
    def __init__(self, dim: int, index_path: Path) -> None:
        self.dim = dim
        self.index_path = index_path
        self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors: np.ndarray) -> None:
        if vectors.size:
            self.index.add(vectors)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        return self.index.search(query_vector.reshape(1, -1), top_k)

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
