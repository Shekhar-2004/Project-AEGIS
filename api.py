from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INCIDENTS = []

# -------------------------------
# API FOR DATA
# -------------------------------
@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    INCIDENTS.append(data)

    if len(INCIDENTS) > 50:
        INCIDENTS.pop(0)

    return {"status": "ok"}

@app.get("/alerts")
def get_alerts():
    return INCIDENTS

@app.get("/stats")
def get_stats():
    stats = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for i in INCIDENTS:
        stats[i["risk_level"]] += 1
    return stats


# -------------------------------
# VIDEO STREAM
# -------------------------------
from src.detection import ObjectDetector
from src.tracking import CentroidTracker

detector = ObjectDetector()
tracker = CentroidTracker()

def generate_frames():
    cap = cv2.VideoCapture("data/videos/test_near_miss.mp4")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))

        # 🔥 DETECTION
        detections = detector.detect(frame)
        tracked_objects = tracker.update(detections)

        # 🔥 DRAW BOXES
        for obj in tracked_objects:
            x1, y1, x2, y2 = obj["bbox"]
            label = f"{obj['class']} #{obj['id']}"

            color = (0, 255, 0) if obj["class"] == "person" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # convert to stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')