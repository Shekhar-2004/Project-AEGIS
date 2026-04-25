# backend/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import os
import hashlib

from backend.services.ai_summary import generate_batch_summaries
from backend.services.aegis_service import analyze_video
from backend.db.session import get_db
from backend.db.incident import Incident

app = FastAPI(title="AEGIS API")

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------------
# HASH FUNCTION (DEDUP)
# -------------------------------
def generate_video_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


@app.get("/")
def root():
    return {"message": "AEGIS API running"}


# -------------------------------
# ANALYZE (WRITE TO DB)
# -------------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        if not file.filename.endswith((".mp4", ".avi", ".mov")):
            raise HTTPException(status_code=400, detail="Invalid file format")

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 HASH-BASED VIDEO ID
        video_id = generate_video_hash(file_path)

        # 🔥 CHECK IF ALREADY PROCESSED
        existing = db.query(Incident).filter(Incident.video_id == video_id).first()

        if existing:
            os.remove(file_path)
            return JSONResponse(content={
                "status": "already_processed",
                "video_id": video_id,
                "message": "Video already analyzed"
            })

        # RUN ANALYSIS
        incidents = analyze_video(file_path)

        os.remove(file_path)

        # 🔥 BATCH GEMINI
        try:
            summaries = generate_batch_summaries(incidents)
        except Exception:
            summaries = ["AI summary unavailable"] * len(incidents)

        # SAVE TO DATABASE
        for inc, summary in zip(incidents, summaries):
            db_incident = Incident(
                video_id=video_id,
                video_source=file.filename,
                object_1=inc["object_1"],
                object_2=inc["object_2"],
                distance_m=inc["distance_m"],
                ttc_seconds=inc["ttc_seconds"],
                relative_velocity=inc["relative_velocity"],
                nmrs_score=inc["nmrs_score"],
                risk_level=inc["risk_level"],
                frame_number=inc["frame_number"],
                ai_summary=summary
            )
            db.add(db_incident)

        db.commit()

        return JSONResponse(content={
            "status": "success",
            "video_id": video_id,
            "total_incidents": len(incidents),
            "data": incidents
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# GET ALL INCIDENTS
# -------------------------------
@app.get("/incidents")
def get_incidents(video_id: str = None, db: Session = Depends(get_db)):
    query = db.query(Incident)

    if video_id:
        query = query.filter(Incident.video_id == video_id)

    data = query.order_by(Incident.id.desc()).all()

    return [
        {
            "video_id": i.video_id,
            "object_1": i.object_1,
            "object_2": i.object_2,
            "distance_m": i.distance_m,
            "ttc_seconds": i.ttc_seconds,
            "relative_velocity": i.relative_velocity,
            "nmrs_score": i.nmrs_score,
            "risk_level": i.risk_level,
            "frame_number": i.frame_number,
            "video_source": i.video_source,
            "ai_summary": i.ai_summary
        }
        for i in data
    ]


# -------------------------------
# GET STATS
# -------------------------------
@app.get("/stats")
def get_stats(video_id: str = None, db: Session = Depends(get_db)):
    query = db.query(Incident)

    if video_id:
        query = query.filter(Incident.video_id == video_id)

    return {
        "LOW": query.filter(Incident.risk_level == "LOW").count(),
        "MEDIUM": query.filter(Incident.risk_level == "MEDIUM").count(),
        "HIGH": query.filter(Incident.risk_level == "HIGH").count(),
    }


# -------------------------------
# GET VIDEOS
# -------------------------------
@app.get("/videos")
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Incident.video_id, Incident.video_source).distinct().all()

    return [
        {
            "video_id": v.video_id,
            "video_name": v.video_source
        }
        for v in videos
    ]


# -------------------------------
# GET VIDEO DATA
# -------------------------------
@app.get("/video/{video_id}")
def get_video_data(video_id: str, db: Session = Depends(get_db)):
    incidents = db.query(Incident)\
        .filter(Incident.video_id == video_id)\
        .order_by(Incident.id.desc())\
        .all()

    if not incidents:
        raise HTTPException(status_code=404, detail="Video not found")

    low = sum(1 for i in incidents if i.risk_level == "LOW")
    medium = sum(1 for i in incidents if i.risk_level == "MEDIUM")
    high = sum(1 for i in incidents if i.risk_level == "HIGH")

    return {
        "video_id": video_id,
        "total_incidents": len(incidents),
        "stats": {
            "LOW": low,
            "MEDIUM": medium,
            "HIGH": high
        },
        "incidents": [
            {
                "id": i.id,
                "object_1": i.object_1,
                "object_2": i.object_2,
                "distance_m": i.distance_m,
                "ttc_seconds": i.ttc_seconds,
                "relative_velocity": i.relative_velocity,
                "nmrs_score": i.nmrs_score,
                "risk_level": i.risk_level,
                "frame_number": i.frame_number,
                "ai_summary": i.ai_summary
            }
            for i in incidents
        ]
    }

# -------------------------------
# GET GRAPH DATA
# -------------------------------
@app.get("/graph-data/{video_id}")
def get_graph_data(video_id: str, db: Session = Depends(get_db)):

    incidents = db.query(Incident)\
        .filter(Incident.video_id == video_id)\
        .all()

    if not incidents:
        raise HTTPException(status_code=404, detail="No data")

    # -------------------------------
    # GRAPH 1: Risk Distribution
    # -------------------------------
    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for i in incidents:
        risk_counts[i.risk_level] += 1

    # -------------------------------
    # GRAPH 2: Distance vs TTC
    # -------------------------------
    distance = [i.distance_m for i in incidents]
    ttc = [i.ttc_seconds for i in incidents]

    # -------------------------------
    # GRAPH 3: NMRS Trend
    # -------------------------------
    nmrs = [i.nmrs_score for i in incidents]

    return {
        "risk_distribution": risk_counts,
        "distance_vs_ttc": {
            "distance": distance,
            "ttc": ttc
        },
        "nmrs_trend": nmrs
    }