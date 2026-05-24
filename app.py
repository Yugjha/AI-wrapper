import streamlit as st
import speech_recognition as sr
import pyttsx3
from io import BytesIO
import os

# Page config
st.set_page_config(
    page_title="AI Wrapper - Voice & Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    h1 {
        color: #58a6ff;
        text-align: center;
        font-size: 3em;
    }
    h2 {
        color: #79c0ff;
        text-align: center;
    }
    .stButton button {
        background-color: #1f6feb;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🤖 AI Wrapper</h1>", unsafe_allow_html=True)
st.markdown("<h2>Academic Intelligence Reimagined</h2>", unsafe_allow_html=True)
st.divider()

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    input_mode = st.radio(
        "Select Input Mode:",
        ["💬 Text Chat", "🎤 Voice Input"],
        key="input_mode"
    )
    
    output_mode = st.radio(
        "Select Output Mode:",
        ["📝 Text Only", "🔊 Voice + Text"],
        key="output_mode"
    )
    
    st.divider()
    st.info("💡 Tip: Test locally first before deploying!")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============================================================
# TEXT CHAT MODE
# ============================================================
if input_mode == "💬 Text Chat":
    st.subheader("💬 Chat Mode")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 📋 Chat History")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.write(f"**You:** {msg['content']}")
            else:
                st.write(f"**AI:** {msg['content']}")
        st.divider()
    
    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Your message:",
            placeholder="Type your question here...",
            height=100,
            key="text_input"
        )
    with col2:
        st.write("")
        st.write("")
        st.write("")
        submit = st.button("📤 Send", use_container_width=True)
    
    if submit and user_input:
        with st.spinner("🔄 Processing..."):
            try:
                # ========== YOUR WRAPPER HERE ==========
                # Replace this with your actual wrapper
                response = f"Echo: {user_input}"
                # response = your_wrapper.process(user_input)
                # ========================================
                
                # Add to history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                st.success("✅ Response received!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================
# VOICE INPUT MODE
# ============================================================
elif input_mode == "🎤 Voice Input":
    st.subheader("🎤 Voice Mode")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Step 1: Record your voice**")
        audio_data = st.audio_input("🎙️ Click to record:")
    
    with col2:
        st.write("**Step 2: Process**")
        if st.button("🔄 Convert Speech to Text", use_container_width=True):
            if audio_data:
                with st.spinner("🔊 Converting speech to text..."):
                    try:
                        # Save audio temporarily
                        with open("temp_audio.wav", "wb") as f:
                            f.write(audio_data.getbuffer())
                        
                        # Recognize speech
                        recognizer = sr.Recognizer()
                        with sr.AudioFile("temp_audio.wav") as source:
                            audio = recognizer.record(source)
                        
                        text = recognizer.recognize_google(audio)
                        st.session_state.voice_text = text
                        st.success("✅ Speech converted!")
                        st.write(f"**Recognized:** {text}")
                        
                        # Cleanup
                        os.remove("temp_audio.wav")
                        
                    except sr.UnknownValueError:
                        st.error("❌ Could not understand audio. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please record audio first!")
    
    st.divider()
    
    # Process converted text
    if "voice_text" in st.session_state:
        st.write(f"**Your Input:** {st.session_state.voice_text}")
        
        if st.button("🤖 Get AI Response", use_container_width=True):
            with st.spinner("🔄 Processing..."):
                try:
                    # ========== YOUR WRAPPER HERE ==========
                    response = f"Response to: {st.session_state.voice_text}"
                    # response = your_wrapper.process(st.session_state.voice_text)
                    # ========================================
                    
                    st.success("✅ Response generated!")
                    st.write(f"**AI Response:** {response}")
                    
                    # Text to Speech
                    if output_mode == "🔊 Voice + Text":
                        st.write("**Playing response...**")
                        try:
                            tts_engine.save_to_file(response, "response.mp3")
                            tts_engine.runAndWait()
                            
                            # Play audio
                            with open("response.mp3", "rb") as audio_file:
                                st.audio(audio_file.read(), format="audio/mp3")
                            
                            os.remove("response.mp3")
                        except Exception as e:
                            st.warning(f"⚠️ Could not generate voice: {e}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.caption("🚀 Built with Streamlit | 🎤 Voice & Chat Enabled | 🤖 AI Powered")
