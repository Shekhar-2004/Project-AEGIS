# src/detection.py

from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.4):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

        # YOLO class names
        self.person_class = "person"
        self.vehicle_classes = {"car", "bus", "truck", "motorcycle"}

    def detect(self, frame):
        detections = []

        results = self.model(frame, verbose=False)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            cls_name = results.names[cls_id]
            confidence = float(box.conf[0])

            if confidence < self.conf_threshold:
                continue

            if cls_name == self.person_class:
                label = "person"
            elif cls_name in self.vehicle_classes:
                label = "vehicle"
            else:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "class": label,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

        return detections
