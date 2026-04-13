
import streamlit as st
from summarizer import summarize_large_text   


st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="centered"
)

#  Title
st.title("🧠 AI Text Summarizer")

#  App Description
st.markdown("""
Welcome to the AI-powered Text Summarizer!

✨ Features:
- Handles large text using chunking  
- Generates concise summaries  
- Built with LangChain + LLM  

👉 Paste your text below and click **Summarize**
""")

# Input Section
st.subheader("📥 Enter Your Text")

user_text = st.text_area(
    label="Paste your text here:",
    height=250,
    placeholder="Example: Paste large article, story, or document here..."
)



#  Button Section
if st.button("🚀 Summarize"):

    # Check if input is empty
    if not user_text.strip():
        st.warning("⚠️ Please enter some text before summarizing.")
    
    else:
       
        with st.spinner("⏳ Summarizing your text... Please wait..."):
            
           
            summary = summarize_large_text(user_text)

        
        st.subheader("📄 Summary")

        
        st.success(summary)

        
        st.markdown("---")

        
        col1, col2 = st.columns(2)

        with col1:
            st.metric("📊 Input Words", len(user_text.split()))

        with col2:
            st.metric("📝 Summary Words", len(summary.split()))

       
        st.markdown("---")
        st.caption("Built using LangChain + Streamlit 🚀")
