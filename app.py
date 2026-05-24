import streamlit as st
from datetime import datetime

# ===== IMPORT YOUR ACTUAL WRAPPER =====
# Uncomment the one you're using:
# from main import AI_Wrapper
# from academic_connector import AcademicConnector
# from your_module import YourClass
# =======================================

st.set_page_config(
    page_title="AI Wrapper - Academic Intelligence",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    h1 { color: #58a6ff; text-align: center; font-size: 3em; }
    h2 { color: #79c0ff; text-align: center; }
    .stButton button {
        background-color: #1f6feb;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    .message-user {
        background-color: #238636;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        color: white;
    }
    .message-ai {
        background-color: #0d47a1;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 AI Wrapper</h1>", unsafe_allow_html=True)
st.markdown("<h2>Academic Intelligence Reimagined</h2>", unsafe_allow_html=True)
st.divider()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    mode = st.radio("Select Mode:", ["💬 Text Chat", "🎤 Voice Chat"])
    st.divider()
    st.info("✅ Your AI Wrapper is Ready!")

# TEXT CHAT MODE
if mode == "💬 Text Chat":
    st.subheader("💬 Chat with AI")
    
    if st.session_state.chat_history:
        st.markdown("### 📋 Conversation")
        for msg in st.session_state.chat_history:
            if msg["type"] == "user":
                st.markdown(f'<div class="message-user"><b>You:</b> {msg["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-ai"><b>AI:</b> {msg["content"]}</div>', 
                           unsafe_allow_html=True)
        st.divider()
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Your message:",
            placeholder="Ask anything about academics, learning, AI...",
            height=100
        )
    with col2:
        st.write("")
        st.write("")
        st.write("")
        submit = st.button("📤 Send", use_container_width=True)
    
    if submit and user_input.strip():
        with st.spinner("🔄 Processing..."):
            try:
                # ===== USE YOUR ACTUAL WRAPPER HERE =====
                # Example:
                # wrapper = AI_Wrapper()
                # ai_response = wrapper.process(user_input)
                
                # For now, demo response:
                ai_response = f"Response: {user_input}"
                # =========================================
                
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": user_input,
                })
                st.session_state.chat_history.append({
                    "type": "ai",
                    "content": ai_response,
                })
                
                st.success("✅ Done!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# VOICE CHAT MODE
elif mode == "🎤 Voice Chat":
    st.subheader("🎤 Voice Mode")
    
    if st.session_state.chat_history:
        st.markdown("### 📋 Conversation")
        for msg in st.session_state.chat_history:
            if msg["type"] == "user":
                st.markdown(f'<div class="message-user"><b>You:</b> {msg["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-ai"><b>AI:</b> {msg["content"]}</div>', 
                           unsafe_allow_html=True)
        st.divider()
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.write("**🎙️ Record your voice:**")
        audio_data = st.audio_input("Click to record")
    
    with col2:
        st.write("**📝 Or type:**")
        voice_text = st.text_input("Type message:", placeholder="Type here...")
    
    if st.button("🤖 Get Response", use_container_width=True):
        input_text = voice_text if voice_text else "Voice message"
        
        if voice_text or audio_data:
            with st.spinner("🔄 Processing..."):
                try:
                    # ===== USE YOUR ACTUAL WRAPPER HERE =====
                    # wrapper = AI_Wrapper()
                    # ai_response = wrapper.process(input_text)
                    
                    ai_response = f"Response to: {input_text}"
                    # =========================================
                    
                    st.session_state.chat_history.append({
                        "type": "user",
                        "content": input_text,
                    })
                    st.session_state.chat_history.append({
                        "type": "ai",
                        "content": ai_response,
                    })
                    
                    st.success("✅ Response generated!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.caption("🚀 Built with Streamlit | 🤖 AI Powered by Yugha")
