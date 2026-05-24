import streamlit as st
from datetime import datetime
from chatbot import PDFChatbot
from llm_client import AVAILABLE_MODELS
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
    .sources-box {
        background-color: #161b22;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #d29922;
    }
    .followup-box {
        background-color: #0d1117;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# Session State Initialization
# ═══════════════════════════════════════════════════════════════

if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = PDFChatbot()
        st.session_state.chatbot_ready = True
    except Exception as e:
        st.session_state.chatbot = None
        st.session_state.chatbot_ready = False
        st.session_state.error = str(e)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "selected_model" not in st.session_state:
    if st.session_state.chatbot_ready:
        st.session_state.selected_model = st.session_state.chatbot.model_config.display_name
    else:
        st.session_state.selected_model = "Not initialized"

# ═══════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════

st.markdown("<h1>📖 Digilab</h1>", unsafe_allow_html=True)
st.markdown("<h2>Media Literacy Chatbot</h2>", unsafe_allow_html=True)
st.divider()

# ═══════════════════════════════════════════════════════════════
# Check Chatbot Status
# ═══════════════════════════════════════════════════════════════

if not st.session_state.chatbot_ready:
    st.error(f"❌ Chatbot initialization failed: {st.session_state.error}")
    st.stop()

# ═══════════════════════════════════════════════════════════════
# Sidebar: Settings & Model Selection
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model Selection
    st.subheader("🤖 AI Model")
    model_options = {
        "⚡ Gemini Flash": "1",
        "🔬 Gemini Pro": "2",
        "🎯 Claude Haiku": "3"
    }
    
    selected_model_display = st.selectbox(
        "Choose Model:",
        options=list(model_options.keys()),
        key="model_select"
    )
    
    model_key = model_options[selected_model_display]
    
    if st.button("🔄 Switch Model", use_container_width=True):
        try:
            new_config = AVAILABLE_MODELS[model_key]
            st.session_state.chatbot.switch_model(new_config)
            st.session_state.selected_model = new_config.display_name
            st.success(f"✅ Switched to {new_config.display_name}")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error switching model: {str(e)}")
    
    st.divider()
    
    # Current Model Info
    st.subheader("📊 Current Model")
    st.info(f"**{st.session_state.chatbot.model_config.display_name}**\n\n{st.session_state.chatbot.model_config.description}")
    
    st.divider()
    
    # Conversation Management
    st.subheader("💬 Conversation")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            try:
                st.session_state.chatbot.clear_history()
                st.session_state.chat_history = []
                st.session_state.last_result = None
                st.success("✅ History cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.metric("Messages", len(st.session_state.chat_history) // 2)
    
    st.divider()
    
    st.caption("✨ Built with Streamlit\n🤖 Powered by Digilab")

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
            result = st.session_state.chatbot.ask_question_with_follow_ups(
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
                "content": result["answer"],
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.last_result = result
            
            st.success("✅ Response received!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error("Traceback:")
            st.code(traceback.format_exc())

# ═══════════════════════════════════════════════════════════════
# Display Last Response Details
# ═══════════════════════════════════════════════════════════════

if st.session_state.last_result:
    st.divider()
    
    # Sources Section
    if st.session_state.last_result.get("sources"):
        with st.expander("📚 Sources Used", expanded=True):
            sources = st.session_state.last_result["sources"]
            st.markdown(f"**Total Sources:** {len(sources)}")
            
            for i, source in enumerate(sources[:5], 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{i}. {source.get('full_section', 'Unknown')[:80]}**")
                        st.caption(f"📄 {source.get('source_file', 'N/A')} | Page {source.get('page', 'N/A')}")
                    with col2:
                        if source.get('text'):
                            st.caption(f"Preview: {source.get('text', '')[:50]}...")
            
            if len(sources) > 5:
                st.info(f"... and {len(sources) - 5} more sources")
    
    # Validation Section
    if st.session_state.last_result.get("validation"):
        with st.expander("✅ Answer Validation"):
            validation = st.session_state.last_result["validation"]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                completeness = validation.get("completeness_score", 0)
                st.metric("Completeness", f"{completeness}/10")
            
            with col2:
                relevance = validation.get("relevance_score", 0)
                st.metric("Relevance", f"{relevance}/10")
            
            with col3:
                accuracy = validation.get("accuracy_score", 0)
                st.metric("Accuracy", f"{accuracy}/10")
    
    # Expanded Queries Section
    if st.session_state.last_result.get("expanded_queries"):
        with st.expander("🔍 Related Queries"):
            for query in st.session_state.last_result["expanded_queries"]:
                if st.button(f"Ask: {query[:70]}...", key=f"query_{query[:20]}"):
                    st.session_state.user_input = query
                    st.rerun()
    
    # Follow-up Questions Section
    if st.session_state.last_result.get("follow_up_questions"):
        follow_ups = st.session_state.last_result["follow_up_questions"]
        type_2_questions = follow_ups.get("type_2_context_aware", [])
        
        if type_2_questions:
            with st.expander("💡 Follow-up Questions"):
                st.markdown(f"**Status:** {follow_ups.get('status', 'unknown')}")
                for i, question in enumerate(type_2_questions, 1):
                    if st.button(
                        f"{i}. {question}",
                        key=f"followup_{i}_{question[:20]}"
                    ):
                        st.session_state.user_input = question
                        st.rerun()

# ═══════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════

st.divider()
st.markdown("""
---
<div style='text-align: center; color: #8b949e;'>
    <p>📖 <b>Digilab Media Literacy Chatbot</b> | 🤖 Powered by AI | 💡 IGNOU Course Assistant</p>
    <p>Built with <b>Streamlit</b> | LLM: <b>Google Gemini + Anthropic Claude</b></p>
</div>
""", unsafe_allow_html=True)
