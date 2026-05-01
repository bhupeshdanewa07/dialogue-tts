import streamlit as st
import requests
import base64
import wave
import io
import os
from dotenv import load_dotenv

load_dotenv()
# Configure the page
st.set_page_config(page_title="Dynamic Dialogue TTS", page_icon="🎙️")

# Sarvam AI TTS Endpoint and Model Configuration
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"
MODEL_NAME = "bulbul:v3"

# Available distinct voices
MALE_VOICES = ["aditya", "amit", "ashutosh", "dev", "kabir", "mohit", "rahul", "rohan", "shubh", "varun"]
FEMALE_VOICES = ["ishita", "kavya", "neha", "niharika", "pooja", "priya", "ritu", "shruti", "simran", "suhani"]
ALL_VOICES = MALE_VOICES + FEMALE_VOICES

def generate_speech(text, speaker, api_key):
    """Calls Sarvam AI API to generate TTS for a single line of text."""
    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_language_code": "en-IN", 
        "speaker": speaker,
        "model": MODEL_NAME
    }
    
    response = requests.post(SARVAM_TTS_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if "audios" in data and data["audios"]:
            return base64.b64decode(data["audios"][0])
    else:
        st.error(f"API Error ({response.status_code}) while generating text: '{text}'\nDetails: {response.text}")
    return None

def combine_wav_audio(wav_bytes_list):
    """Stitches multiple WAV byte strings into a single contiguous WAV file."""
    if not wav_bytes_list:
        return None
    
    data_frames = []
    
    # Extract audio parameters from the first clip
    with wave.open(io.BytesIO(wav_bytes_list[0]), 'rb') as w:
        params = w.getparams()
        data_frames.append(w.readframes(w.getnframes()))
    
    # Extract frames from subsequent clips
    for wav_bytes in wav_bytes_list[1:]:
        with wave.open(io.BytesIO(wav_bytes), 'rb') as w:
            data_frames.append(w.readframes(w.getnframes()))
            
    # Write all frames to a new in-memory file
    combined_audio = io.BytesIO()
    with wave.open(combined_audio, 'wb') as w:
        w.setparams(params)
        for frames in data_frames:
            w.writeframes(frames)
            
    return combined_audio.getvalue()

# --- UI Layout ---

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #A0AEC0;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎙️ Studio Voice Synthesizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bring your scripts to life with AI-powered multi-voice synthesis</div>', unsafe_allow_html=True)

# API Key Input
api_key = os.getenv("SARVAM_API_KEY")

st.markdown("### 📝 1. Enter Your Dialogue")
# Default dialogue placeholder
default_dialogue = """John: Have you finished the API integration yet?
Sarah: Almost done. I just need to fix a small routing bug in FastAPI.
John: Awesome. Let me know when it's pushed to GitHub.
Sarah: Will do. It should be up in about ten minutes."""

dialogue_input = st.text_area("Write your script using the format 'Name: Text'", value=default_dialogue, height=200)

# Extract characters dynamically for the UI
characters = []
if dialogue_input.strip():
    for line in dialogue_input.strip().split('\n'):
        if line.strip() and ':' in line:
            char = line.split(':', 1)[0].strip()
            if char and char not in characters:
                characters.append(char)

st.markdown("### 🎭 2. Assign Character Voices")
voice_mapping = {}

if characters:
    # Create an aesthetic card-like layout for voice mapping
    with st.container():
        cols = st.columns(min(len(characters), 4))
        for idx, char in enumerate(characters):
            col_idx = idx % 4
            with cols[col_idx]:
                st.markdown(f"**{char}**")
                
                # 1. Select Gender
                gender = st.selectbox(
                    "Gender",
                    ["👨 Male", "👩 Female"],
                    index=0 if idx % 2 == 0 else 1,
                    key=f"gender_{char}",
                    label_visibility="collapsed"
                )
                
                # 2. Select Voice based on Gender
                if "Male" in gender:
                    voice_options = MALE_VOICES
                else:
                    voice_options = FEMALE_VOICES
                    
                selected_voice = st.selectbox(
                    "Voice", 
                    voice_options, 
                    key=f"voice_{char}",
                    label_visibility="collapsed"
                )
                
                st.caption(f"Voice: {selected_voice.title()}")
                voice_mapping[char] = selected_voice
else:
    st.info("Start typing your dialogue above to detect characters and assign voices.")

st.markdown("### 🎧 3. Generate Audio")
if st.button("✨ Generate Cinematic Audio", type="primary", use_container_width=True):
    if not api_key:
        st.error("🚨 Please set your SARVAM_API_KEY in the .env file.")
    elif not characters:
        st.warning("⚠️ Could not detect any characters. Make sure the format is 'Name: Dialogue'.")
    else:
        st.success(f"**Active Mapping:** " + " | ".join([f"{char} ➡️ `{voice}`" for char, voice in voice_mapping.items()]))
        
        lines = dialogue_input.strip().split('\n')
        audio_segments = []
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 2. Generate Audio Segment by Segment
        total_lines = len([l for l in lines if l.strip() and ':' in l])
        processed_lines = 0
        
        for idx, line in enumerate(lines):
            if not line.strip() or ':' not in line:
                continue
                
            character, text = line.split(':', 1)
            character = character.strip()
            text = text.strip()
            
            if not text:
                continue
            
            speaker_voice = voice_mapping.get(character, ALL_VOICES[0])
            
            status_text.text(f"Generating speech for {character}...")
            
            # Fetch audio
            wav_bytes = generate_speech(text, speaker_voice, api_key)
            
            if wav_bytes:
                audio_segments.append(wav_bytes)
            else:
                st.error(f"Failed to generate audio for line: {line}")
                st.stop()
                
            processed_lines += 1
            progress_bar.progress(processed_lines / total_lines)
            
        status_text.text("Stitching audio files together...")
        
        # 3. Stitch and Output
        if audio_segments:
            final_audio = combine_wav_audio(audio_segments)
            
            status_text.empty()
            progress_bar.empty()
            
            st.balloons()
            st.success("✅ Audio generated successfully!")
            
            # Display audio player prominently
            st.audio(final_audio, format="audio/wav")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.download_button(
                    label="💾 Download WAV File",
                    data=final_audio,
                    file_name="studio_dialogue_output.wav",
                    mime="audio/wav",
                    use_container_width=True
                )