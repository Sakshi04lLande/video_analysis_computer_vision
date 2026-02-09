

```markdown
#  Computer Vision + GenAI Video Analysis System

##  Project Overview
This project is an AI-powered video analytics system that combines **Computer Vision (YOLOv8 + BoT-SORT tracking)** with **Generative AI (LLM-based summarization)** to analyze human movement patterns in videos.

The system detects and tracks people in video streams, analyzes their movement behavior, and automatically generates human-readable reports and PDF summaries.

---

##  Key Features
 Real-time People Detection using YOLOv8  
 Multi-object Tracking using BoT-SORT  
 Entry / Exit Time Logging  
 Movement Direction Detection (Left / Right / Up / Down / Standing)  
 Speed Classification (Standing / Slow / Normal / Fast)  
 LLM-based Scene Summary Generation  
 Automated PDF Report Generation  

---

##  AI + Tech Stack
- Python  
- OpenCV  
- Ultralytics YOLOv8  
- BoT-SORT Tracker  
- Azure OpenAI / LLM Integration  
- ReportLab (PDF Generation)  
- Pandas / NumPy  

---

##  Project Structure
```

project/
│
├ people_tracking.py        # Main tracking pipeline
├ gen.py                    # LLM summary generator
├ generate_pdf.py           # PDF report generator
├ botsort.yaml              # Tracker config
├ requirements.txt          # Dependencies
├ README.md

````



###  Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```


---

###  Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  How To Run Project

### Step 1 — Run Tracking

```bash
python people_tracking.py
```

Generates:

* detections.json
* detections_summary.json
* people_entry_exit_log.csv

---

### Step 2 — Generate AI Summary

```bash
python gen.py
```

Generates:

* analysis.txt

---

### Step 3 — Generate Final PDF Report

```bash
python generate_pdf.py
```

Generates:

* video_analysis_report.pdf

---

##  Output Example

The system generates:

* Scene-level movement summary
* Key person behavior insights
* Crowd movement patterns
* Person-wise entry / exit logs
* Professional PDF report

---

## Important Notes

 Large video files are NOT included in repo
 YOLO model weights are NOT included

Download YOLO weights manually from:
[https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)

---

##  Future Improvements

* Real-time dashboard visualization
* Cloud deployment
* Multi-camera tracking
* Behavior anomaly detection
* REST API integration

---



