# main.py

import cv2
from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector
from src.tracking import CentroidTracker


def main():
    cap = open_video(0)
    detector = ObjectDetector()
    tracker = CentroidTracker()

    while True:
        ret, frame = read_frame(cap)
        if not ret:
            break

        detections = detector.detect(frame)
        tracked_objects = tracker.update(detections)

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

        cv2.imshow("Tracking Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    release_video(cap)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
