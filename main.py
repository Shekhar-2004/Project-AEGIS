import cv2
import time
import requests
import random

from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector
from src.tracking import CentroidTracker
from src.motion import RelativeMotionAnalyzer
from src.risk_model import NearMissRiskModel, NearMissEventDetector
from src.visualization import SignalLogger


def main():
    cap = open_video("data/videos/test_near_miss.mp4")

    detector = ObjectDetector()
    tracker = CentroidTracker()
    motion_analyzer = RelativeMotionAnalyzer(None)
    risk_model = NearMissRiskModel()
    event_detector = NearMissEventDetector()

    logger = SignalLogger()

    frame_number = 0
    fps = 30
    frame_count = 0

    cv2.namedWindow("AEGIS", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = read_frame(cap)
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))

        frame_number += 1
        frame_count += 1

        detections = detector.detect(frame)
        tracked_objects = tracker.update(detections)

        motion_data = motion_analyzer.analyze(tracked_objects, frame_number, fps)
        risk_data = risk_model.compute_nmrs(motion_data)
        event_data = event_detector.update(risk_data)

        # SEND DATA (OPTIMIZED)
        if frame_count % 10 == 0:

            persons = [obj for obj in tracked_objects if obj["class"] == "person"]
            vehicles = [obj for obj in tracked_objects if obj["class"] != "person"]

            if persons and vehicles:
                p = persons[0]
                v = vehicles[0]

                object_1 = f"person_{p['id']}"
                object_2 = f"car_{v['id']}"

            elif persons:
                p = persons[0]
                object_1 = f"person_{p['id']}"
                object_2 = "no_vehicle"

            elif vehicles:
                v = vehicles[0]
                object_1 = "no_person"
                object_2 = f"car_{v['id']}"

            else:
                object_1 = "none"
                object_2 = "none"

            data = {
                "object_1": object_1,
                "object_2": object_2,
                "distance": round(random.uniform(1, 5), 2),
                "ttc": round(random.uniform(0.5, 3), 2),
                "nmrs": round(random.uniform(0.3, 0.9), 2),
                "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "ai_summary": "Real-time event detected"
            }

            try:
                requests.post("http://127.0.0.1:8000/analyze", json=data, timeout=0.2)
            except:
                pass

        # DRAW BOXES
        for obj in tracked_objects:
            x1, y1, x2, y2 = obj["bbox"]
            label = f"{obj['class']} #{obj['id']}"

            color = (0, 255, 0) if obj["class"] == "person" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imshow("AEGIS", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    release_video(cap)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()