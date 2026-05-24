import streamlit as st
from your_wrapper import AI_Wrapper  # Import your AI wrapper

st.set_page_config(page_title="AI Wrapper", layout="wide")

# Header
st.markdown("""
    <div style="text-align: center;">
    <h1>Academic Intelligence</h1>
    <h2>Reimagined.</h2>
    <p>Empowering learning through advanced AI-driven intelligence.</p>
    </div>
""", unsafe_allow_html=True)

# Initialize your AI wrapper
wrapper = AI_Wrapper()

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_area("Enter your query:", placeholder="Ask me anything...")
with col2:
    submit = st.button("🚀 Submit", use_container_width=True)

# Process and display results
if submit and user_input:
    with st.spinner("Processing..."):
        result = wrapper.process(user_input)
        st.success("Done!")
        st.write(result)

# Sidebar
st.sidebar.title("Settings")
st.sidebar.info("This is your AI Wrapper deployed!")
