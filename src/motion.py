# src/motion.py

import math
import time


class RelativeMotionAnalyzer:
    def __init__(self):
        # Stores previous distance and time for each pair
        self.pair_states = {}

    def _distance(self, c1, c2):
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def analyze(self, tracked_objects):
        """
        Computes distance, relative velocity, and TTC
        for each pedestrian–vehicle pair.
        """
        results = []
        current_time = time.time()

        persons = [o for o in tracked_objects if o["class"] == "person"]
        vehicles = [o for o in tracked_objects if o["class"] == "vehicle"]

        for p in persons:
            for v in vehicles:
                pair_key = (p["id"], v["id"])

                distance = self._distance(p["centroid"], v["centroid"])

                if pair_key in self.pair_states:
                    prev = self.pair_states[pair_key]
                    dt = current_time - prev["time"]

                    if dt > 0:
                        velocity = (prev["distance"] - distance) / dt
                    else:
                        velocity = 0.0
                else:
                    velocity = 0.0
                    dt = None

                # Time-to-Collision (only if approaching)
                if velocity > 0:
                    ttc = distance / velocity
                else:
                    ttc = float("inf")

                # Update state
                self.pair_states[pair_key] = {
                    "distance": distance,
                    "time": current_time
                }

                results.append({
                    "person_id": p["id"],
                    "vehicle_id": v["id"],
                    "distance": distance,
                    "relative_velocity": velocity,
                    "ttc": ttc
                })

        return results
