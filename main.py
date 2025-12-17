# main.py

import cv2
from src.video_io import open_video, read_frame, release_video
from src.detection import ObjectDetector


def main():
    cap = open_video(0)
    detector = ObjectDetector()

    while True:
        ret, frame = read_frame(cap)
        if not ret:
            break

        detections = detector.detect(frame)

        # Draw bounding boxes
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = det["class"]

            color = (0, 255, 0) if label == "person" else (0, 0, 255)

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

        cv2.imshow("Detection Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    release_video(cap)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
