import requests
import streamlit as st

st.set_page_config(page_title="LangGraph Test")

st.title("LangGraph Streaming Test")

prompt = st.text_area(
    "Enter Prompt",
    height=150
)

if st.button("Generate"):

    if not prompt.strip():
        st.warning("Please enter a prompt")
        st.stop()

    with st.spinner("Generating..."):

        response = requests.post(
            "http://localhost:8000/generate",
            json={
                "prompt": prompt
            },
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

    st.subheader("Response")

    st.write(data["generated_text"])