# backend/services/aegis_service.py

from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector
from src.tracking import CentroidTracker
from src.motion import RelativeMotionAnalyzer
from src.risk_model import NearMissRiskModel, NearMissEventDetector
import numpy as np
import cv2


# Homography Matrix
H = np.array([
    [-1.26050328e+00, -2.28373535e+00, 252.471392],
    [-0.0794548289, 3.36358776, -369.915199],
    [0.0245924746, -0.788755349, 1.0]
])


def analyze_video(video_path: str):
    try:
        cap = open_video(video_path)

        if cap is None:
            print("Error: Could not open video.")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30

        detector = ObjectDetector()
        tracker = CentroidTracker()
        motion = RelativeMotionAnalyzer(H)
        risk = NearMissRiskModel()
        event = NearMissEventDetector()

        best_events = {}
        frame_idx = 0

        while True:
            ret, frame = read_frame(cap)
            if not ret:
                break

            frame_idx += 1

            detections = detector.detect(frame)
            tracked = tracker.update(detections)
            motion_data = motion.analyze(tracked, frame_idx, fps)

            if not motion_data:
                continue

            risk_data = risk.compute_nmrs(motion_data)
            event_data = event.update(risk_data)

            for e in event_data:
                if not e.get("near_miss", False):
                    continue

                key = (e["person_id"], e["vehicle_id"])
                nmrs = float(e["smooth_nmrs"])

                ttc_val = e["ttc"]
                if ttc_val == float("inf") or ttc_val > 10:
                    ttc_val = None
                else:
                    ttc_val = float(ttc_val)

                if key not in best_events or nmrs > best_events[key]["nmrs_score"]:
                    best_events[key] = {
                        "object_1": str(f"person_{e['person_id']}"),
                        "object_2": str(f"vehicle_{e['vehicle_id']}"),
                        "distance_m": float(round(e["distance"], 3)),
                        "ttc_seconds": ttc_val,
                        "relative_velocity": float(round(e["relative_velocity"], 3)),
                        "nmrs_score": float(round(nmrs, 3)),
                        "risk_level": "HIGH" if nmrs > 0.7 else "MEDIUM",
                        "frame_number": int(frame_idx)
                    }

        release_video(cap)

        incidents = list(best_events.values())

        print("Total incidents:", len(incidents))

        return incidents

    except Exception as e:
        print("ERROR in analyze_video:", str(e))
        return []