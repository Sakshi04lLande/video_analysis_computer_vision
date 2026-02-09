import cv2
import pandas as pd
from ultralytics import YOLO
from datetime import datetime
import numpy as np

# ============================
# CONFIG
# ============================
VIDEO_PATH = "input_video.mp4"
OUTPUT_CSV = "people_entry_exit_log.csv"
MODEL_PATH = "yolov8l.pt"

CONF_THRESH = 0.30
MIN_W, MIN_H = 40, 90
TIMEOUT_FRAMES = 40   # 1–1.5 sec

print("🚀 Stable ID People Tracker (BoT-SORT + Smart ReID)...")

# ============================
# LOAD YOLO
# ============================
model = YOLO(MODEL_PATH)

# ============================
# OPEN VIDEO
# ============================
cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame = cap.read()
H, W = frame.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# ============================
# TRACKING MEMORY
# ============================
people = {}          # raw_id → info
serial_id_map = {}   # raw_id → stable small ID
next_serial_id = 1

frame_num = 0

# ============================
# MAIN LOOP
# ============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_num += 1

    # --- YOLO + BOT-SORT ---
    results = model.track(
        frame,
        conf=CONF_THRESH,
        persist=True,
        tracker="botsort.yaml",
        verbose=False
    )
    r = results[0]

    visible_raw_ids = set()

    if r.boxes.id is not None:
        ids = r.boxes.id.cpu().numpy().astype(int)
        boxes = r.boxes.xyxy.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy().astype(int)

        for box, raw_id, conf, cls in zip(boxes, ids, confs, classes):

            if cls != 0:
                continue

            x1, y1, x2, y2 = map(int, box)
            w, h = x2 - x1, y2 - y1

            clear = (
                conf >= CONF_THRESH and
                w >= MIN_W and
                h >= MIN_H
            )

            visible_raw_ids.add(raw_id)

            # -------- Stable ID Assignment --------
            if raw_id not in serial_id_map:
                serial_id_map[raw_id] = next_serial_id
                next_serial_id += 1

            stable_id = serial_id_map[raw_id]

            # -------- Track Entry / Last Seen --------
            if raw_id not in people:
                people[raw_id] = {
                    "entry": datetime.now().strftime("%H:%M:%S"),
                    "exit": None,
                    "last_seen": frame_num
                }
                print(f"🟢 ENTRY → ID {stable_id}")

            people[raw_id]["last_seen"] = frame_num

            # -------- Draw only if CLEAR --------
            if clear:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"ID {stable_id}", (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # -------- EXIT detection using timeout --------
    for raw_id in list(people.keys()):
        if people[raw_id]["exit"] is None:
            if frame_num - people[raw_id]["last_seen"] > TIMEOUT_FRAMES:
                people[raw_id]["exit"] = datetime.now().strftime("%H:%M:%S")
                print(f"🔴 EXIT → ID {serial_id_map[raw_id]}")

    cv2.imshow("Stable People Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ============================
# SAVE CSV
# ============================
rows = []
for raw_id, info in people.items():
    rows.append({
        "Person_ID": serial_id_map[raw_id],
        "Entry_Time": info["entry"],
        "Exit_Time": info["exit"]
    })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)
print("✅ Log saved:", OUTPUT_CSV)
