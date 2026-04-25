from fastapi import APIRouter
from backend.services.aegis_service import analyze_video

router = APIRouter()

@router.post("/analyze")
def analyze(video_path: str):
    results = analyze_video(video_path)
    return {"incidents": results}