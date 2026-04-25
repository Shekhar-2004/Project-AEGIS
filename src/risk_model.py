# src/risk_model.py

import numpy as np


class NearMissRiskModel:
    def compute_nmrs(self, motion_data):
        results = []

        for m in motion_data:
            d = max(m["distance"], 0.1)
            v = max(m["relative_velocity"], 0.0)
            ttc = m["ttc"]

            if ttc == float("inf") or ttc <= 0:
                ttc = 10.0

            ttc = np.clip(ttc, 0.1, 10.0)

            risk = (
                0.5 * (1 / d) +
                0.3 * v +
                0.2 * (1 / ttc)
            )

            nmrs = np.tanh(risk)

            results.append({**m, "nmrs": float(nmrs)})

        return results


class NearMissEventDetector:
    def __init__(self):
        self.states = {}

    def update(self, risk_data):
        results = []

        for r in risk_data:
            key = (r["person_id"], r["vehicle_id"])
            nmrs = r["nmrs"]
            d = r["distance"]
            v = r["relative_velocity"]

            if key not in self.states:
                self.states[key] = {
                    "count": 0,
                    "active": False
                }

            state = self.states[key]

            if nmrs > 0.5 or (d < 1.0 and v > 0):
                state["count"] += 1
            else:
                state["count"] = max(0, state["count"] - 1)

            if state["count"] >= 2:
                state["active"] = True

            results.append({
                **r,
                "smooth_nmrs": nmrs,
                "near_miss": state["active"]
            })

        return results