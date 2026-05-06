# Tactical Surveillance AI

An AI-powered video surveillance system that scans drone and CCTV footage to detect targets using natural language queries, with automated email alerting.

**Live Demo:** [Click here]
(https://surveillance-ai-rtnpt47fa6vjkqvmshj7qw.streamlit.app/)

---

## Overview

Tactical Surveillance AI is a computer vision tool built for security and defense applications. Upload any video file, describe your target in plain English, and the system scans the footage frame by frame to identify the best match — returning the exact timestamp and sending an automated email alert with the detected frame.

---

## Features

- **Natural Language Target Search** — Describe any target in plain English (e.g., "A white ambulance", "Person in red jacket") without needing to configure classifiers or labels
- **Frame Extraction with Timestamp Mapping** — Automatically extracts one frame per second from uploaded video and maps each frame to its exact timestamp
- **CLIP-Based Semantic Matching** — Uses OpenAI's CLIP vision-language model to semantically match the text query against each extracted frame
- **Confidence Scoring** — Displays a cosine similarity score indicating detection confidence
- **Automated Email Alerts** — On successful detection, sends an email notification containing the confidence score, timestamp, and the detected frame as an attachment
- **Supports Drone and CCTV Footage** — Accepts MP4 and AVI video formats

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Streamlit | Web application framework |
| CLIP (ViT-B-32) | Vision-language model for semantic image-text matching |
| Sentence Transformers | Embedding generation and cosine similarity |
| OpenCV | Video processing and frame extraction |
| Pillow | Image handling |
| Python | Core language |

---

## Project Structure

```
defense-rag-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- A Gmail account with App Password enabled (for email alerts)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/KhushiMaheshwari101/defense-rag-chatbot.git
cd defense-rag-chatbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure email credentials**

Open `app.py` and update the following variables:
```python
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_gmail_app_password"
RECEIVER_EMAIL = "receiver_email@gmail.com"
```

> To generate a Gmail App Password: Google Account > Security > 2-Step Verification > App Passwords

**4. Run the application**
```bash
streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`

---

## Usage

1. Upload a drone or CCTV video file (MP4 or AVI)
2. Enter a plain English description of the target in the search box
3. Click **Start Intelligence Scan**
4. The system extracts frames, scans each one, and returns the best match with its timestamp
5. If confidence exceeds the threshold, an email alert is automatically sent

---

## Deployment

This project is deployed on **Streamlit Cloud**.

To deploy your own instance:
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select this repository
4. Set `app.py` as the main file
5. Add your email credentials directly in `app.py` before deploying
6. Click **Deploy**

---

## Demoshots


<img width="1874" height="1045" alt="image" src="https://github.com/user-attachments/assets/75cdf1e0-095c-46c1-a5b4-6371337bf972" />
<img width="1780" height="967" alt="image" src="https://github.com/user-attachments/assets/1020b934-396d-4d11-a856-588f67109bb0" />



---

## Author

**Khushi Maheshwari**

[GitHub](https://github.com/KhushiMaheshwari101)

---

If you found this project useful, consider giving it a star.
