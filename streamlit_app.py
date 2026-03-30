import streamlit as st
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import io

# Load environment variables
load_dotenv()

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Configuration
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George
TTS_MODEL = "eleven_v3"
STT_MODEL = "scribe_v1"

# Page configuration
st.set_page_config(
    page_title="ElevenLabs Studio",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .logo {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
    }
    .stButton>button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>ElevenLabs Studio</h1>
    <p class="subtitle">Powered by ElevenLabs AI</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'tts_audio' not in st.session_state:
    st.session_state.tts_audio = None
if 'stt_text' not in st.session_state:
    st.session_state.stt_text = None
if 'tts_status' not in st.session_state:
    st.session_state.tts_status = None
if 'stt_status' not in st.session_state:
    st.session_state.stt_status = None

# Create tabs
tab1, tab2 = st.tabs(["Text to Speech", "Speech to Text"])

# Text to Speech Tab
with tab1:
    st.header("Text to Speech")

    # Text input
    text_input = st.text_area(
        "Enter text to convert to speech:",
        placeholder="Type or paste your text here...",
        height=150,
        help="Enter the text you want to convert to speech"
    )

    # Character count
    char_count = len(text_input)
    st.caption(f"Characters: {char_count:,}")

    # Convert button
    if st.button("Convert to Speech", key="tts_button", disabled=not text_input.strip()):
        with st.spinner("Converting text to speech..."):
            try:
                # Call ElevenLabs TTS API
                audio_generator = client.text_to_speech.convert(
                    text=text_input.strip(),
                    voice_id=VOICE_ID,
                    model_id=TTS_MODEL,
                    output_format="mp3_44100_128",
                )

                # Convert generator to bytes
                audio_bytes = b"".join(audio_generator)
                st.session_state.tts_audio = audio_bytes
                st.session_state.tts_status = "success"

            except Exception as e:
                st.session_state.tts_status = "error"
                st.error(f"Error: {str(e)}")

    # Display status messages
    if st.session_state.tts_status == "success":
        st.markdown('<div class="success-message">✅ Audio generated successfully!</div>', unsafe_allow_html=True)
    elif st.session_state.tts_status == "error":
        st.markdown('<div class="error-message">❌ Failed to generate audio. Please try again.</div>', unsafe_allow_html=True)

    # Display audio player and download
    if st.session_state.tts_audio:
        st.subheader("Audio Output")

        # Audio player
        st.audio(st.session_state.tts_audio, format="audio/mp3")

        # Download button
        st.download_button(
            label="⬇ Download MP3",
            data=st.session_state.tts_audio,
            file_name="speech.mp3",
            mime="audio/mpeg",
            key="download_tts"
        )

# Speech to Text Tab
with tab2:
    st.header("Speech to Text")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload an audio file to transcribe:",
        type=["mp3", "wav", "m4a", "ogg", "flac", "mp4"],
        help="Supported formats: MP3, WAV, M4A, OGG, FLAC, MP4"
    )

    # Display file info
    if uploaded_file:
        file_size = len(uploaded_file.getvalue())
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1048576:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / 1048576:.1f} MB"

        st.info(f"📄 {uploaded_file.name} ({size_str})")

    # Transcribe button
    if st.button("Transcribe Audio", key="stt_button", disabled=not uploaded_file):
        with st.spinner("Transcribing audio..."):
            try:
                # Call ElevenLabs STT API
                result = client.speech_to_text.convert(
                    file=(uploaded_file.name, io.BytesIO(uploaded_file.getvalue())),
                    model_id=STT_MODEL,
                )

                st.session_state.stt_text = result.text
                st.session_state.stt_status = "success"

            except Exception as e:
                st.session_state.stt_status = "error"
                st.error(f"Error: {str(e)}")

    # Display status messages
    if st.session_state.stt_status == "success":
        st.markdown('<div class="success-message">✅ Transcription complete!</div>', unsafe_allow_html=True)
    elif st.session_state.stt_status == "error":
        st.markdown('<div class="error-message">❌ Failed to transcribe audio. Please try again.</div>', unsafe_allow_html=True)

    # Display transcription
    if st.session_state.stt_text:
        st.subheader("Transcription")
        st.text_area(
            "Transcribed text:",
            value=st.session_state.stt_text,
            height=150,
            disabled=True
        )

        # Download transcription
        st.download_button(
            label="⬇ Download TXT",
            data=st.session_state.stt_text,
            file_name="transcription.txt",
            mime="text/plain",
            key="download_stt"
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "ElevenLabs Studio &mdash; Text to Speech & Speech to Text"
    "</div>",
    unsafe_allow_html=True
)