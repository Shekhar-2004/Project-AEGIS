# src/motion.py

import math
import numpy as np


class RelativeMotionAnalyzer:
    def __init__(self, homography_matrix):
        self.pair_states = {}
        self.H = homography_matrix
        self.active_pair = None

    def _project_to_ground(self, p):
    # If no homography matrix, return original point
        if self.H is None:
            return p

        import numpy as np

        p = np.array([p[0], p[1], 1])
        p_transformed = self.H @ p
        p_transformed /= p_transformed[2]
        return p_transformed[:2]

    def _distance(self, c1, c2):
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def analyze(self, tracked_objects, frame_number, fps):
        persons = [o for o in tracked_objects if o["class"] == "person"]
        vehicles = [o for o in tracked_objects if o["class"] == "vehicle"]

        if not persons or not vehicles:
            return []

        best_pair = None

        # keep same pair
        if self.active_pair:
            p_id, v_id = self.active_pair
            p = next((x for x in persons if x["id"] == p_id), None)
            v = next((x for x in vehicles if x["id"] == v_id), None)

            if p and v:
                p_g = self._project_to_ground(p["centroid"])
                v_g = self._project_to_ground(v["centroid"])
                if p_g and v_g:
                    best_pair = (p, v, p_g, v_g)

        # find closest
        if best_pair is None:
            min_d = float("inf")
            for p in persons:
                for v in vehicles:
                    p_g = self._project_to_ground(p["centroid"])
                    v_g = self._project_to_ground(v["centroid"])

                    if p_g is None or v_g is None:
                        continue

                    d = self._distance(p_g, v_g)
                    if d < min_d:
                        min_d = d
                        best_pair = (p, v, p_g, v_g)

            if best_pair is None:
                return []

            self.active_pair = (best_pair[0]["id"], best_pair[1]["id"])

        p, v, p_g, v_g = best_pair
        distance = self._distance(p_g, v_g)
        key = (p["id"], v["id"])

        t = frame_number / fps

        prev_v = 0.0
        if key in self.pair_states:
            prev = self.pair_states[key]
            dt = t - prev["time"]

            if dt > 0.001:
                raw_v = (prev["distance"] - distance) / dt
                prev_v = prev.get("velocity", 0.0)
                velocity = 0.7 * prev_v + 0.3 * raw_v
            else:
                velocity = prev_v
        else:
            velocity = 0.0

        ttc = distance / velocity if velocity > 0 else float("inf")

        self.pair_states[key] = {
            "distance": distance,
            "time": t,
            "velocity": velocity
        }

        return [{
            "person_id": p["id"],
            "vehicle_id": v["id"],
            "distance": distance,
            "relative_velocity": velocity,
            "ttc": ttc
        }]