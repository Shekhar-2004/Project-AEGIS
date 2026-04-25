# src/visualization.py

import os
import matplotlib.pyplot as plt


class SignalLogger:
    def __init__(self):
        self.time = []
        self.distance = []
        self.ttc = []
        self.nmrs = []

    def log(self, t, distance, ttc, nmrs):
        self.time.append(t)
        self.distance.append(distance)
        self.ttc.append(ttc)
        self.nmrs.append(nmrs)

    def plot_all(self, save_dir="data/outputs"):
        os.makedirs(save_dir, exist_ok=True)

        # ---------- Time vs NMRS ----------
        fig = plt.figure()
        plt.plot(self.time, self.nmrs)
        plt.xlabel("Time (s)")
        plt.ylabel("NMRS")
        plt.title("Time vs Near-Miss Risk Score")
        plt.grid(True)
        fig.savefig(os.path.join(save_dir, "time_vs_nmrs.png"))
        plt.close(fig)

        # ---------- Time vs TTC ----------
        fig = plt.figure()
        plt.plot(self.time, self.ttc)
        plt.xlabel("Time (s)")
        plt.ylabel("TTC (s)")
        plt.title("Time vs Time-to-Collision")
        plt.grid(True)
        fig.savefig(os.path.join(save_dir, "time_vs_ttc.png"))
        plt.close(fig)

        # ---------- Distance vs NMRS ----------
        fig = plt.figure()
        plt.plot(self.distance, self.nmrs)
        plt.xlabel("Distance (pixels)")
        plt.ylabel("NMRS")
        plt.title("Distance vs Risk")
        plt.grid(True)
        fig.savefig(os.path.join(save_dir, "distance_vs_nmrs.png"))
        plt.close(fig)

        # Optional: show all at once AFTER saving
        plt.show()
