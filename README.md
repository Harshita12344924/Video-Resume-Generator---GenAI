🎥 **AI Video Resume Generator**
An end-to-end AI-powered application that takes a user's resume (in PDF format) and generates a talking video resume using Google's Gemini AI for summarization and HeyGen API for AI avatar video synthesis.



🛠️ **Tech Stack**
* Frontend: Streamlit
* Backend AI: Google Gemini 1.5 Flash
              HeyGen API
* PDF Parsing: PyPDF2
* Deployment Ready: Easily deploy on Streamlit Cloud or locally



📂 **Features**
* Upload a PDF Resume
* Automatically summarizes your resume with Gemini AI
* Generates a video of an AI avatar speaking your resume summary using HeyGen
* Real-time status polling to fetch video after generation
* Downloadable video resume link



🚀 **Getting Started**

**1. Clone the Repository**
git clone https://github.com/your-username/video-resume-generator.git
cd video-resume-generator

**2. Install Dependencies**
Make sure you have Python 3.8+ and run:
pip install streamlit google-generativeai PyPDF2 requests

**3. Run the App**
streamlit run video_resume_app.py



🔐 **API Keys Required**
This project uses two APIs:

**1. Google Generative AI (Gemini)**
Get your API key from Google AI Studio

Replace in the code:

GENAI_API_KEY = "your-gemini-api-key"

**2. HeyGen API**
Sign up at HeyGen and get an API key.

Replace in the code:

HEYGEN_API_KEY = "your-heygen-api-key"

AVATAR_ID = "your-avatar-id"

VOICE_ID = "your-voice-id"

You can choose different avatars and voices from HeyGen’s documentation.



📸 **Sample Output**
The generated video will be:
* 1280x720 resolution
* Neutral background
* 16:9 aspect ratio
* Talking AI avatar presenting your resume summary
