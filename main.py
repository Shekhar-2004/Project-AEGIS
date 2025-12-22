# main.py

import cv2
import time

from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector
from src.tracking import CentroidTracker
from src.motion import RelativeMotionAnalyzer
from src.risk_model import NearMissRiskModel, NearMissEventDetector
from src.visualization import SignalLogger


def main():
    # -------------------------------
    # Initialize components
    # -------------------------------
    cap = open_video("data/videos/test_near_miss.mp4")  # Use webcam; replace with video file path if needed

    detector = ObjectDetector()
    tracker = CentroidTracker()
    motion_analyzer = RelativeMotionAnalyzer()
    risk_model = NearMissRiskModel()
    event_detector = NearMissEventDetector()

    logger = SignalLogger()
    start_time = time.time()

    # -------------------------------
    # Main processing loop
    # -------------------------------
    while True:
        ret, frame = read_frame(cap)
        if not ret:
            print("End of video stream or cannot read frame.")
            break

        # ---- Step 2: Detection ----
        detections = detector.detect(frame)

        # ---- Step 3: Tracking ----
        tracked_objects = tracker.update(detections)

        # ---- Step 4: Relative Motion ----
        motion_data = motion_analyzer.analyze(tracked_objects)

        # ---- Step 5: Risk Modeling ----
        risk_data = risk_model.compute_nmrs(motion_data)

        # ---- Step 6: Temporal Smoothing & Event Detection ----
        event_data = event_detector.update(risk_data)

        # -------------------------------
        # Visualization: bounding boxes
        # -------------------------------
        for obj in tracked_objects:
            x1, y1, x2, y2 = obj["bbox"]
            label = f"{obj['class']} #{obj['id']}"

            color = (0, 255, 0) if obj["class"] == "person" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        # -------------------------------
        # Visualization: risk info
        # -------------------------------
        near_miss_active = False

        for idx, e in enumerate(event_data):
            text = (
                f"P{e['person_id']}–V{e['vehicle_id']} | "
                f"NMRS={e['smooth_nmrs']:.2f}"
            )

            color = (0, 0, 255) if e["near_miss"] else (0, 255, 255)

            cv2.putText(
                frame,
                text,
                (10, 30 + idx * 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            if e["near_miss"]:
                near_miss_active = True

        if near_miss_active:
            cv2.putText(
                frame,
                "NEAR MISS DETECTED",
                (50, frame.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                3
            )

        # -------------------------------
        # Step 7: Signal Logging (most risky pair)
        # -------------------------------
        if event_data:
            most_risky = max(event_data, key=lambda x: x["smooth_nmrs"])

            logger.log(
                t=time.time() - start_time,
                distance=most_risky["distance"],
                ttc=most_risky["ttc"],
                nmrs=most_risky["smooth_nmrs"]
            )

        # -------------------------------
        # Display
        # -------------------------------
        cv2.imshow("Near-Miss Risk Estimation System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # -------------------------------
    # Cleanup & plots
    # -------------------------------
    release_video(cap)
    cv2.destroyAllWindows()

    # Generate graphs after demo ends
    logger.plot_all()


if __name__ == "__main__":
    main()
