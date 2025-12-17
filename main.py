# main.py

import cv2

from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector
from src.tracking import CentroidTracker
from src.motion import RelativeMotionAnalyzer
from src.risk_model import NearMissRiskModel


def main():
    # -------------------------------
    # Initialize system components
    # -------------------------------
    cap = open_video(0)  # 0 = webcam, or replace with video file path

    detector = ObjectDetector()
    tracker = CentroidTracker()
    motion_analyzer = RelativeMotionAnalyzer()
    risk_model = NearMissRiskModel()

    # -------------------------------
    # Main processing loop
    # -------------------------------
    while True:
        ret, frame = read_frame(cap)
        if not ret:
            print("End of video stream or cannot read frame.")
            break

        # Step 2: Detection
        detections = detector.detect(frame)

        # Step 3: Tracking
        tracked_objects = tracker.update(detections)

        # Step 4: Relative motion analysis
        motion_data = motion_analyzer.analyze(tracked_objects)
        
        #Step 5: NMRS calculation
        risk_data = risk_model.compute_nmrs(motion_data)

        # -------------------------------
        # Visualization
        # -------------------------------
        # Draw tracked objects
        for obj in tracked_objects:
            x1, y1, x2, y2 = obj["bbox"]
            obj_id = obj["id"]
            label = f"{obj['class']} #{obj_id}"

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

        # Overlay relative motion signals (temporary debug view)
        for idx, m in enumerate(motion_data):
            text = (
                f"P{m['person_id']}–V{m['vehicle_id']} | "
                f"d={m['distance']:.1f} "
                f"v={m['relative_velocity']:.2f} "
                f"TTC={m['ttc']:.2f}"
            )

            cv2.putText(
                frame,
                text,
                (10, 30 + idx * 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1
            )
            
        #Calculation
        for idx, r in enumerate(risk_data):
         text = (
        f"P{r['person_id']}–V{r['vehicle_id']} | "
        f"NMRS={r['nmrs']:.2f}"
        )

         cv2.putText(
            frame,
            text,
            (10, 30 + idx * 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )


        cv2.imshow("Near-Miss System – Motion Signals", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # -------------------------------
    # Cleanup
    # -------------------------------
    release_video(cap)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
