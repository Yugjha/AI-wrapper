import streamlit as st
import sys
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Wrapper - Academic Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    h1 {
        color: #58a6ff;
        text-align: center;
        font-size: 3.5em;
        margin-bottom: 0;
    }
    h2 {
        color: #79c0ff;
        text-align: center;
        font-size: 2em;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.1em;
        margin-bottom: 2em;
    }
    .stButton button {
        background-color: #1f6feb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #388bfd;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1>Academic Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Reimagined.</h2>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Empowering learning through advanced AI-driven intelligence.</p>', 
                unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.info("🤖 AI Wrapper Interface")
    
    mode = st.radio(
        "Select Mode:",
        ["Chat", "Query", "Analysis"],
        key="mode_selector"
    )
    
    st.divider()
    
    temperature = st.slider(
        "Response Creativity:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    max_tokens = st.slider(
        "Response Length:",
        min_value=50,
        max_value=2000,
        value=500,
        step=50
    )

# Main Content
st.subheader(f"📝 {mode} Mode")

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_area(
        "Enter your query:",
        placeholder="Ask me anything about academics, learning, or AI...",
        height=120,
        key="user_input"
    )

with col2:
    st.write("")
    st.write("")
    submit_button = st.button("🚀 Submit", use_container_width=True)

st.divider()

# Process input
if submit_button and user_input:
    with st.spinner("🔄 Processing your query..."):
        try:
            # ============================================
            # MODIFY THIS SECTION WITH YOUR ACTUAL WRAPPER
            # ============================================
            
            # Example: Simple echo (replace with your actual wrapper)
            result = f"Response to: {user_input}"
            
            # If you have a real wrapper, use something like:
            # from your_module import YourWrapperClass
            # wrapper = YourWrapperClass()
            # result = wrapper.process(user_input, temperature=temperature)
            
            # ============================================
            
            st.success("✅ Done!")
            
            st.markdown("### 📤 Response:")
            st.write(result)
            
            # Additional options
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("👍 Helpful", key="helpful")
            with col2:
                st.button("👎 Not Helpful", key="not_helpful")
            with col3:
                st.button("🔄 Regenerate", key="regenerate")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Make sure your wrapper module is properly configured.")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📚 Built with Streamlit")
with col2:
    st.caption("🤖 Powered by AI")
with col3:
    st.caption("💡 Created by Yugha")
