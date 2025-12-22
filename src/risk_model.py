# src/risk_model.py

import math


class NearMissRiskModel:
    def __init__(
        self,
        d0=150.0,       # distance scaling (pixels)
        v_max=200.0,    # max relative velocity
        tau=2.0,        # TTC scaling
        alpha=0.4,
        beta=0.3,
        gamma=0.3
    ):
        self.d0 = d0
        self.v_max = v_max
        self.tau = tau

        # weights must sum to 1
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def compute_nmrs(self, motion_data):
        """
        motion_data: list of dicts from RelativeMotionAnalyzer
        returns: list of dicts with NMRS added
        """
        results = []

        for m in motion_data:
            d = m["distance"]
            v = max(m["relative_velocity"], 0.0)
            ttc = m["ttc"]

            # Risk components
            R_d = math.exp(-d / self.d0)
            R_v = min(v / self.v_max, 1.0)
            R_ttc = math.exp(-ttc / self.tau) if ttc != float("inf") else 0.0

            nmrs = (
                self.alpha * R_d +
                self.beta * R_v +
                self.gamma * R_ttc
            )

            results.append({
                **m,
                "R_d": R_d,
                "R_v": R_v,
                "R_ttc": R_ttc,
                "nmrs": nmrs
            })

        return results
    
    
class NearMissEventDetector:
    def __init__(
        self,
        alpha=0.6,           # EMA smoothing factor
        risk_threshold=0.6,  # NMRS threshold
        persistence=5        # frames
    ):
        self.alpha = alpha
        self.risk_threshold = risk_threshold
        self.persistence = persistence
        self.states = {}

    def update(self, risk_data):
        """
        risk_data: output from NearMissRiskModel
        returns: list with near-miss event info
        """
        results = []

        for r in risk_data:
            key = (r["person_id"], r["vehicle_id"])
            nmrs = r["nmrs"]

            if key not in self.states:
                self.states[key] = {
                    "smooth_nmrs": nmrs,
                    "above_count": 0,
                    "active": False
                }

            state = self.states[key]

            # EMA smoothing
            state["smooth_nmrs"] = (
                self.alpha * nmrs +
                (1 - self.alpha) * state["smooth_nmrs"]
            )

            # Threshold persistence logic
            if state["smooth_nmrs"] > self.risk_threshold:
                state["above_count"] += 1
            else:
                state["above_count"] = 0
                state["active"] = False

            # Declare near-miss
            if state["above_count"] >= self.persistence:
                state["active"] = True

            results.append({
                **r,
                "smooth_nmrs": state["smooth_nmrs"],
                "near_miss": state["active"]
            })

        return results

