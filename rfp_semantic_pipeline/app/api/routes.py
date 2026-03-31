from fastapi import APIRouter, File, UploadFile

from app.core.pipeline import PipelineService

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/pipeline/run")
async def run_pipeline(files: list[UploadFile] = File(...)) -> dict:
    service = PipelineService()
    workspace_id = service.create_workspace()
    payload = []
    for file in files:
        payload.append((file.filename, await file.read()))
    documents = service.ingest_files(workspace_id, payload)
    return service.run(workspace_id, documents)
