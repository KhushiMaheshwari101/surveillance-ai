%%writefile app.py
import streamlit as st
import cv2, os, smtplib, glob, re, time
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from email.message import EmailMessage

# --- 1. CONFIG ---
SENDER_EMAIL = "maheshwarikhushi36@gmail.com"
APP_PASSWORD = "vest pgpk wjbk lrvn"
RECEIVER_EMAIL = "maheshwarikhushi36@gmail.com"

@st.cache_resource
def load_model():
    return SentenceTransformer('clip-ViT-B-32')

def send_alert(target, score, frame_path, timestamp):
    msg = EmailMessage()
    msg.set_content(f"🚨 TARGET DETECTED!\n\nObject: {target}\nConfidence: {score:.2f}\nSpotted at: {timestamp}")
    msg['Subject'] = f"Tactical Alert: {target} at {timestamp}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    with open(frame_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=f'target_{timestamp.replace(":","-")}.jpg')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

# --- 2. UI SETUP ---
st.set_page_config(page_title="Tactical AI v2", layout="wide")
st.title("🛡️ Tactical Surveillance AI (with Time-Mapping)")

video_file = st.file_uploader("Upload Drone/CCTV Video", type=['mp4', 'avi'])
query = st.text_input("Search Target:", "A white ambulance")

if st.button("🚀 Start Intelligence Scan") and video_file:
    model = load_model()

    # Video Save logic
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.getbuffer())

    # Folder Cleanup
    output_folder = 'tactical_frames'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    for f in glob.glob(f"{output_folder}/*.jpg"): os.remove(f)

    # A. VIDEO EXTRACTION (THE MISSING PART)
    st.info("🎬 Step 1: Video Extraction & Timestamp Mapping...")
    cap = cv2.VideoCapture("temp_video.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    progress_text = st.empty()
    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Har 1 second mein 1 frame nikaalo accuracy ke liye
        if frame_count % int(fps) == 0:
            seconds = int(frame_count / fps)
            # Filename mein time encode kar diya
            cv2.imwrite(f"{output_folder}/time_{seconds}s.jpg", frame)
            saved_count += 1
        frame_count += 1
        if frame_count % 100 == 0:
            progress_text.text(f"Processing... {int((frame_count/total_frames)*100)}%")

    cap.release()
    st.success(f"✅ Extracted {saved_count} frames with temporal metadata.")

    # B. AI SEARCH
    st.info(f"🔎 Step 2: AI Scanning for '{query}'...")
    image_files = sorted(glob.glob(f"{output_folder}/*.jpg"))
    text_emb = model.encode([query])

    best_score, best_frame, best_time = -1, "", "00:00"

    for img_path in image_files:
        img_emb = model.encode(Image.open(img_path))
        score = util.cos_sim(img_emb, text_emb).item()
        if score > best_score:
            best_score = score
            best_frame = img_path
            # Time nikaalo filename se
            secs = int(re.search(r"time_(\d+)s", img_path).group(1))
            best_time = f"{secs // 60:02d}:{secs % 60:02d}"

    # C. FINAL ALERT
    if best_score > 0.22:
        st.subheader(f"🎯 Target Spotted at {best_time}")
        col1, col2 = st.columns(2)
        with col1:
            st.image(best_frame, caption=f"Detection Frame (Confidence: {best_score:.2f})")
        with col2:
            st.metric("Confidence Score", f"{best_score:.2f}")
            st.write("📤 Sending Tactical Email Notification...")
            send_alert(query, best_score, best_frame, best_time)
            st.success("Alert Sent Successfully!")
    else:
        st.error("No high-confidence target detected. Try a more descriptive query.")
