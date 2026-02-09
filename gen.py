import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_VERSION = os.getenv("AZURE_OPENAI_VERSION")

DETECTIONS_JSON = "detections.json"

client = AzureOpenAI(
    api_version=AZURE_VERSION,
    api_key=AZURE_KEY,
    azure_endpoint=AZURE_ENDPOINT,
)

# -----------------------------------------
# LOAD FRAME-BY-FRAME DATA
# -----------------------------------------
frames = json.load(open(DETECTIONS_JSON, "r"))

# Build per-person timeline from raw frame data
person_timeline = {}

for frame_data in frames:
    frame_num = frame_data["frame"]

    for obj in frame_data["objects"]:
        pid = obj["id"]

        if pid not in person_timeline:
            person_timeline[pid] = {
                "first_frame": frame_num,
                "last_frame": frame_num,
                "movement": [],
                "speed": [],
                "centers": []
            }

        person_timeline[pid]["last_frame"] = frame_num
        person_timeline[pid]["movement"].append(obj["direction"])
        person_timeline[pid]["speed"].append(obj["speed"])
        person_timeline[pid]["centers"].append(obj["center"])

# -----------------------------------------
# COMPRESS TIMELINE FOR LLM
# -----------------------------------------
compressed = {}
for pid, data in person_timeline.items():
    compressed[pid] = {
        "person_id": pid,
        "first_frame": data["first_frame"],
        "last_frame": data["last_frame"],
        "dominant_direction": max(set(data["movement"]), key=data["movement"].count),
        "avg_speed": max(set(data["speed"]), key=data["speed"].count),
        "movement_samples": data["movement"][:20],  # first 20 frames sample
        "speed_samples": data["speed"][:20]         # first 20 frames sample
    }

# -----------------------------------------
# LLM PROMPT
# -----------------------------------------
prompt = f"""
You are an expert video analyst.

Generate a SHORT and CLEAN summary.  
This summary must fit within **1 page**.

IMPORTANT RULES:
- KEEP IT VERY SHORT.
- NO per-frame details.
- NO timeline for every person.
- ONLY describe the 5–7 most important people.
- NO tables.
- NO markdown tables.
- Bullet points only.
- No stories. No long explanations.

Write 4 short sections:

1. SHORT Scene Summary (3–4 lines)
2. Key Person Movements (only major people, 1 line each)
3. Short Timeline Overview (general movement pattern, not per-person)
4. Crowd-Level Behavior (3–4 lines)

Data:
{json.dumps(compressed, indent=2)}
"""
# -----------------------------------------
# LLM CALL
# -----------------------------------------
response = client.chat.completions.create(
    model=AZURE_DEPLOYMENT,
    messages=[{"role": "user", "content": prompt}]
)

final_summary = response.choices[0].message.content

open("analysis.txt", "w", encoding="utf-8").write(final_summary)
print("\n📄 analysis.txt saved\n")
