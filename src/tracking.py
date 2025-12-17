# src/tracking.py

import math


class CentroidTracker:
    def __init__(self, max_distance=50, max_missed=5):
        self.next_id = 0
        self.objects = {}
        self.max_distance = max_distance
        self.max_missed = max_missed

    def _centroid(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def _distance(self, c1, c2):
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def update(self, detections):
        updated_objects = {}
        used_ids = set()

        for det in detections:
            bbox = det["bbox"]
            cls = det["class"]
            centroid = self._centroid(bbox)

            min_dist = float("inf")
            matched_id = None

            for obj_id, obj in self.objects.items():
                if obj["class"] != cls or obj_id in used_ids:
                    continue

                dist = self._distance(centroid, obj["centroid"])
                if dist < min_dist and dist < self.max_distance:
                    min_dist = dist
                    matched_id = obj_id

            if matched_id is not None:
                updated_objects[matched_id] = {
                    "id": matched_id,
                    "class": cls,
                    "centroid": centroid,
                    "bbox": bbox,
                    "missed": 0
                }
                used_ids.add(matched_id)
            else:
                new_id = self.next_id
                self.next_id += 1
                updated_objects[new_id] = {
                    "id": new_id,
                    "class": cls,
                    "centroid": centroid,
                    "bbox": bbox,
                    "missed": 0
                }
                used_ids.add(new_id)

        # Handle missed objects
        for obj_id, obj in self.objects.items():
            if obj_id not in used_ids:
                obj["missed"] += 1
                if obj["missed"] <= self.max_missed:
                    updated_objects[obj_id] = obj

        self.objects = updated_objects
        return list(self.objects.values())
