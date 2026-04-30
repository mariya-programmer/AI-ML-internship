import streamlit as st
import cv2
import json
import hashlib
import numpy as np
import os
from ultralytics import YOLO
from PIL import Image
import tempfile

# ---------------------------
# CONFIG
# ---------------------------
MODEL_PATH = "yolov8n.pt"   # Change to best.pt if you have custom model

# ---------------------------
# SESSION STATE
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------
# USER AUTH FUNCTIONS
# ---------------------------

def load_users():
    if not os.path.exists("users.json"):
        return {}
    try:
        with open("users.json", "r") as f:
            content = f.read().strip()
            if content == "":
                return {}
            return json.loads(content)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

# ---------------------------
# LOAD MODEL SAFELY
# ---------------------------

@st.cache_resource
def load_model():
    try:
        return YOLO(MODEL_PATH)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        st.stop()

model = load_model()

# ---------------------------
# UI
# ---------------------------

st.title("🔐 Custom Object Detection System")

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if menu == "Register":
        st.subheader("Create Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account Created Successfully!")
            else:
                st.error("Username already exists!")

    elif menu == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

# ---------------------------
# AFTER LOGIN
# ---------------------------

else:

    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    option = st.selectbox(
        "Select Detection Mode",
        ["Live Webcam Detection", "Image Upload Detection", "Video Detection"]
    )

    # ---------------------------
    # LIVE WEBCAM
    # ---------------------------

    if option == "Live Webcam Detection":

        run = st.checkbox("Start Webcam")
        FRAME_WINDOW = st.image([])

        if run:
            cap = cv2.VideoCapture(0)

            while run:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to access webcam")
                    break

                results = model(frame, conf=0.3)
                annotated_frame = results[0].plot()

                FRAME_WINDOW.image(annotated_frame, channels="BGR")

            cap.release()

    # ---------------------------
    # IMAGE UPLOAD
    # ---------------------------

    elif option == "Image Upload Detection":

        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            image_np = np.array(image)

            results = model(image_np, conf=0.3)
            annotated = results[0].plot()

            st.image(annotated, channels="BGR")

            # Confidence analysis
            if len(results[0].boxes) > 0:
                confidences = results[0].boxes.conf.cpu().numpy()
                avg_conf = np.mean(confidences)
                st.write(f"Average Confidence: {avg_conf:.2f}")

    # ---------------------------
    # VIDEO DETECTION
    # ---------------------------

    elif option == "Video Detection":

        uploaded_video = st.file_uploader("Upload Video", type=["mp4"])

        if uploaded_video:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_video.read())

            cap = cv2.VideoCapture(tfile.name)
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = model(frame, conf=0.3)
                annotated_frame = results[0].plot()

                stframe.image(annotated_frame, channels="BGR")

            cap.release()