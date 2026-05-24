import streamlit as st
from datetime import datetime
import traceback

# ═══════════════════════════════════════════════════════════════
# Page Config
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Digilab — Media Literacy Chatbot",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# Custom CSS
# ═══════════════════════════════════════════════════════════════

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
    }
    .message-user {
        background-color: #238636;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: white;
        border-left: 4px solid #3fb950;
    }
    .message-ai {
        background-color: #0d47a1;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        color: white;
        border-left: 4px solid #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# Initialize Chatbot with Safe Error Handling
# ═══════════════════════════════════════════════════════════════

@st.cache_resource
def load_chatbot():
    try:
        from chatbot import PDFChatbot
        return PDFChatbot(), None
    except ImportError as e:
        return None, f"Import Error: {str(e)}"
    except Exception as e:
        return None, f"Initialization Error: {str(e)}"

chatbot, init_error = load_chatbot()

# ═══════════════════════════════════════════════════════════════
# Session State Initialization
# ═══════════════════════════════════════════════════════════════

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ═══════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════

st.markdown("<h1>📖 Digilab</h1>", unsafe_allow_html=True)
st.markdown("<h2>Media Literacy Chatbot</h2>", unsafe_allow_html=True)
st.divider()

# ═══════════════════════════════════════════════════════════════
# Error Handling
# ═══════════════════════════════════════════════════════════════

if chatbot is None:
    st.error("❌ Chatbot initialization failed!")
    st.error(f"Error: {init_error}")
    st.info("⚠️ Checking dependencies...")
    
    # Show what's wrong
    st.write("### Possible Issues:")
    st.write("1. **Google Generative AI**: Missing or incorrectly imported")
    st.write("2. **API Keys**: Check your `.env` file for:")
    st.code("""
    GOOGLE_API_KEY=your_key_here
    ANTHROPIC_API_KEY=your_key_here
    PINECONE_API_KEY=your_key_here
    """)
    st.write("3. **Data Files**: Ensure `data/processed/txt_processed.flag` exists")
    st.write("4. **Dependencies**: Check logs for missing packages")
    
    st.stop()

# ═══════════════════════════════════════════════════════════════
# Sidebar Settings
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("⚙️ Settings")
    
    # Current Model
    try:
        current_model = chatbot.model_config.display_name if chatbot else "Unknown"
    except:
        current_model = "Default"
    
    st.subheader("🤖 AI Model")
    st.info(f"**Current:** {current_model}")
    
    st.divider()
    
    # Clear History
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        try:
            chatbot.clear_history()
            st.session_state.chat_history = []
            st.session_state.last_result = None
            st.success("✅ History cleared!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    st.metric("Messages", len(st.session_state.chat_history) // 2)
    st.caption("✨ Built with Streamlit")

# ═══════════════════════════════════════════════════════════════
# Main Chat Area
# ═══════════════════════════════════════════════════════════════

st.subheader("💬 Chat with Your Chatbot")

# Display Chat History
if st.session_state.chat_history:
    st.markdown("### 📋 Conversation")
    for msg in st.session_state.chat_history:
        if msg["type"] == "user":
            st.markdown(
                f'<div class="message-user"><b>You:</b> {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message-ai"><b>Assistant:</b> {msg["content"]}</div>',
                unsafe_allow_html=True
            )
    st.divider()

# Input Area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_area(
        "Your Question:",
        placeholder="Ask about media literacy, digital citizenship, or any course topic...",
        height=100,
        key="user_input"
    )

with col2:
    st.write("")
    st.write("")
    st.write("")
    submit_button = st.button("📤 Send", use_container_width=True, type="primary")

st.divider()

# ═══════════════════════════════════════════════════════════════
# Process User Input
# ═══════════════════════════════════════════════════════════════

if submit_button and user_input.strip():
    with st.spinner("🔄 Thinking..."):
        try:
            # Call the chatbot
            result = chatbot.ask_question_with_follow_ups(
                question=user_input.strip(),
                use_history=True
            )
            
            # Store in history
            st.session_state.chat_history.append({
                "type": "user",
                "content": user_input.strip(),
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.chat_history.append({
                "type": "assistant",
                "content": result.get("answer", "No response"),
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.last_result = result
            
            st.success("✅ Response received!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            with st.expander("📋 Full Error Details"):
                st.code(traceback.format_exc())

# ═══════════════════════════════════════════════════════════════
# Display Last Response Details
# ═══════════════════════════════════════════════════════════════

if st.session_state.last_result:
    st.divider()
    
    # Sources
    if st.session_state.last_result.get("sources"):
        with st.expander("📚 Sources Used"):
            sources = st.session_state.last_result["sources"]
            st.write(f"**Total:** {len(sources)} section(s)")
            for i, source in enumerate(sources[:5], 1):
                st.write(f"**{i}.** {source.get('full_section', 'Unknown')[:80]}")
                st.caption(f"📄 {source.get('source_file', 'N/A')} | Page {source.get('page', 'N/A')}")
    
    # Follow-up Questions
    if st.session_state.last_result.get("follow_up_questions"):
        follow_ups = st.session_state.last_result["follow_up_questions"]
        type_2 = follow_ups.get("type_2_context_aware", [])
        if type_2:
            with st.expander("💡 Follow-up Questions"):
                for i, q in enumerate(type_2, 1):
                    if st.button(f"{i}. {q}", key=f"fup_{i}"):
                        st.session_state.user_input = q
                        st.rerun()

# ═══════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════

st.divider()
st.markdown("""
---
<div style='text-align: center; color: #8b949e;'>
    <p>📖 <b>Digilab Media Literacy Chatbot</b></p>
    <p>Built with Streamlit | Powered by Google Gemini & Anthropic Claude</p>
</div>
""", unsafe_allow_html=True)
