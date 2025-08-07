import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import requests
import time
import json
import os

# ---- Configuration ----
GENAI_API_KEY = ""
HEYGEN_API_KEY = ""
AVATAR_ID = ""
VOICE_ID = ""

# ---- Setup Gemini ----
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- Streamlit App ----
st.set_page_config(page_title="AI Video Resume Generator", layout="centered")
st.title("🎥 AI Video Resume Generator")
st.write("Upload your resume and generate a talking video resume with AI.")

# ---- File Upload ----
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully!")
    
    # ---- Extract Text from PDF ----
    pdf_reader = PdfReader(uploaded_file)
    resume_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    
    # ---- Summarize Resume ----
    st.subheader("🔍 Generating Summary using Gemini AI...")
    with st.spinner("Thinking..."):
        response = model.generate_content(f"Summarize this resume for a professional video resume:\n\n{resume_text}")
        summary = response.text.strip()
    st.text_area("🧠 Summary:", summary, height=200)

    if st.button("🎬 Generate Video Resume"):
        st.subheader("Generating Video using HeyGen...")
        
        headers = {
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": AVATAR_ID,
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": summary,
                        "voice_id": VOICE_ID,
                        "speed": 1.0
                    },
                    "background": {
                        "type": "color",
                        "value": "#FFFFFF"
                    }
                }
            ],
            "dimension": {"width": 1280, "height": 720},
            "title": "Video Resume",
            "aspect_ratio": "16:9",
            "test": True
        }

        res = requests.post("https://api.heygen.com/v2/video/generate", headers=headers, json=payload)

        if res.status_code == 200:
            video_id = res.json()["data"]["video_id"]
            st.success(f"Video generation started! Video ID: {video_id}")

            # ---- Poll for Status ----
            video_url = None
            for i in range(20):
                time.sleep(20)
                status_res = requests.get(
                    f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
                    headers=headers
                )

                try:
                    status_json = status_res.json()
                except json.JSONDecodeError:
                    st.error("Invalid JSON received while polling.")
                    break

                if status_json.get("data", {}).get("status") == "completed":
                    video_url = status_json["data"]["video_url"]
                    break
                elif status_json.get("data", {}).get("status") == "failed":
                    st.error("❌ Video generation failed.")
                    break
                st.info(f"Polling... Attempt {i+1}/20")

            if video_url:
                st.success("✅ Video Ready!")
                st.video(video_url)
                st.markdown(f"[🔗 Download Video]({video_url})", unsafe_allow_html=True)
            else:
                st.warning("Video generation timed out. Try again later.")
        else:
            st.error(f"❌ Error from HeyGen API: {res.status_code}")
