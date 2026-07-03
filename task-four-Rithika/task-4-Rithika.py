"""
AI-Powered Smart Traffic Management System
Uses YOLOv5 for vehicle detection + Random Forest for congestion prediction
to dynamically adjust traffic signal timings.
"""

import cv2
import torch
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import time
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# 1. VEHICLE DETECTION  (YOLOv5)
# ─────────────────────────────────────────────

class VehicleDetector:
    """Detects and counts vehicles in a frame using YOLO."""

    VEHICLE_CLASSES = {
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck"
    }

    def __init__(self, confidence=0.4):
        print("[INFO] Loading YOLO model...")
        from ultralytics import YOLO
        self.model = YOLO("yolov8n.pt")
        self.confidence = confidence
        print("[INFO] YOLO loaded successfully.")

    def detect(self, frame):

        results = self.model(frame)

        count = 0
        annotated = frame.copy()

        for r in results:

            boxes = r.boxes

            for box in boxes:

                cls = int(box.cls[0])

                if cls in self.VEHICLE_CLASSES:

                    conf = float(box.conf[0])

                    if conf < self.confidence:
                        continue

                    count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    label = f"{self.VEHICLE_CLASSES[cls]} {conf:.2f}"

                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        annotated,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

        cv2.putText(
            annotated,
            f"Vehicles: {count}",
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        return annotated, count, None

# ─────────────────────────────────────────────
# 2. CONGESTION PREDICTOR  (Random Forest)
# ─────────────────────────────────────────────

class CongestionPredictor:
    """
    Predicts congestion level (Low / Medium / High) from traffic features.
    Can be trained on synthetic data or a real CSV dataset.
    """

    LEVELS = {0: "Low", 1: "Medium", 2: "High"}

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.trained = False

    # ── Synthetic dataset (fallback when no real data exists) ──
    @staticmethod
    def _generate_data(n=1000):
        np.random.seed(42)
        vehicle_count = np.random.randint(0, 60, n)
        hour           = np.random.randint(0, 24, n)
        day_of_week    = np.random.randint(0, 7,  n)
        speed_kmh      = np.clip(60 - vehicle_count * 0.8 + np.random.randn(n) * 5, 5, 60)

        # Rule-based labels
        labels = np.where(vehicle_count < 15, 0,
                 np.where(vehicle_count < 35, 1, 2))

        return pd.DataFrame({
            "vehicle_count": vehicle_count,
            "hour":          hour,
            "day_of_week":   day_of_week,
            "avg_speed":     speed_kmh,
            "congestion":    labels
        })

    def train(self, csv_path=None):
        """Train on a CSV file or fall back to synthetic data."""
        if csv_path:
            df = pd.read_csv(csv_path)
            print(f"[INFO] Loaded dataset: {csv_path} ({len(df)} rows)")
        else:
            df = self._generate_data()
            print("[INFO] Using synthetic training data.")
            
        features = ["vehicle_count", "hour", "day_of_week", "avg_speed"]
        X = df[features]
        y = df["congestion"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        self.trained = True

        preds = self.model.predict(X_test)
        print("\n[EVALUATION]\n" + classification_report(
            y_test, preds, target_names=list(self.LEVELS.values())))

    def predict(self, vehicle_count, hour, day_of_week, avg_speed=30.0):
        """Return congestion label string."""
        if not self.trained:
            raise RuntimeError("Model not trained. Call train() first.")
        features = np.array([[vehicle_count, hour, day_of_week, avg_speed]])
        level_id = self.model.predict(features)[0]
        return self.LEVELS[level_id]


# ─────────────────────────────────────────────
# 3. SIGNAL TIMING OPTIMIZER
# ─────────────────────────────────────────────

class SignalOptimizer:
    """
    Converts vehicle counts / congestion levels into green-light durations.
    Formula: base + weight × count, capped at max.
    """

    TIMING = {
        "Low":    {"green": 20, "yellow": 3, "red": 40},
        "Medium": {"green": 40, "yellow": 4, "red": 30},
        "High":   {"green": 60, "yellow": 5, "red": 20},
    }

    @staticmethod
    def calculate(vehicle_count, congestion_level):
        base_timing = SignalOptimizer.TIMING.get(congestion_level,
                                                  SignalOptimizer.TIMING["Medium"])
        extra = min(vehicle_count // 5, 20)          # +1 s per 5 vehicles, max +20 s
        green  = base_timing["green"]  + extra
        yellow = base_timing["yellow"]
        red    = max(base_timing["red"] - extra, 10) # red shrinks as green grows

        return {"green": green, "yellow": yellow, "red": red,
                "congestion": congestion_level, "vehicle_count": vehicle_count}


# ─────────────────────────────────────────────
# 4. TRAFFIC MANAGEMENT SYSTEM  (orchestrator)
# ─────────────────────────────────────────────

class TrafficManagementSystem:
    """
    Ties together detection → prediction → signal optimization.
    Supports three input modes: webcam, video file, single image.
    """

    def __init__(self, dataset_csv=None):
        self.detector  = VehicleDetector()
        self.predictor = CongestionPredictor()
        self.optimizer = SignalOptimizer()

        print("[INFO] Training congestion predictor...")
        self.predictor.train(dataset_csv)

    # ── helpers ───────────────────────────────
    def _overlay_signal(self, frame, signal_info):
        """Draw a semi-transparent HUD on the frame."""
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (340, 160), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

        c = signal_info["congestion"]
        colour = {"Low": (0,200,0), "Medium": (0,165,255), "High": (0,0,255)}[c]

        lines = [
            f"Vehicles  : {signal_info['vehicle_count']}",
            f"Congestion: {c}",
            f"Green     : {signal_info['green']} s",
            f"Yellow    : {signal_info['yellow']} s",
            f"Red       : {signal_info['red']} s",
        ]
        for i, txt in enumerate(lines):
            cv2.putText(frame, txt, (10, 30 + i * 26),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, colour, 2)
        return frame

    def _process_frame(self, frame):
        now = time.localtime()
        annotated, count, _ = self.detector.detect(frame)
        congestion = self.predictor.predict(count, now.tm_hour, now.tm_wday)
        signal     = self.optimizer.calculate(count, congestion)
        result     = self._overlay_signal(annotated, signal)

        print(f"  Vehicles={count:3d} | Congestion={congestion:6s} | "
              f"Green={signal['green']}s  Yellow={signal['yellow']}s  Red={signal['red']}s")
        return result, signal

    # ── public API ────────────────────────────
    def process_image(self, image_path, save_path=None):
        """Detect & optimise signal for a single image."""
        frame = cv2.imread(image_path)
        if frame is None:
            raise FileNotFoundError(f"Cannot open image: {image_path}")

        result, signal = self._process_frame(frame)
        cv2.imshow("Traffic Analysis", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if save_path:
            cv2.imwrite(save_path, result)
            print(f"[INFO] Saved: {save_path}")
        return signal

    def process_video(self, video_path, save_path=None):
        """Run on a video file, frame by frame."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        writer = None
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(save_path, fourcc, fps, (w, h))

        frame_no = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_no += 1
            if frame_no % 5 != 0:   # process every 5th frame for speed
                continue

            print(f"Frame {frame_no:5d} |", end=" ")
            result, _ = self._process_frame(frame)

            if writer:
                writer.write(result)

            cv2.imshow("Traffic Analysis", result)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("[INFO] Quit by user.")
                break

        cap.release()
        if writer:
            writer.release()
            print(f"[INFO] Output saved: {save_path}")
        cv2.destroyAllWindows()

    def run_webcam(self, camera_id=0):
        """Live processing from webcam."""
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_id}")

        print("[INFO] Press 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result, _ = self._process_frame(frame)
            cv2.imshow("Live Traffic", result)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


# ─────────────────────────────────────────────
# 5. ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Smart Traffic Management System")
    parser.add_argument("--mode",    choices=["webcam", "video", "image"],
                        default="webcam", help="Input mode")
    parser.add_argument("--input",   type=str, default=None,
                        help="Path to video/image file (not needed for webcam)")
    parser.add_argument("--output",  type=str, default=None,
                        help="Optional path to save annotated output")
    parser.add_argument("--dataset", type=str, default=None,
                        help="Optional CSV for congestion model training")
    args = parser.parse_args()

    system = TrafficManagementSystem(dataset_csv=args.dataset)

    if args.mode == "webcam":
        system.run_webcam()
    elif args.mode == "video":
        if not args.input:
            parser.error("--input required for video mode")
        system.process_video(args.input, args.output)
    elif args.mode == "image":
        if not args.input:
            parser.error("--input required for image mode")
        system.process_image(args.input, args.output)
