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

    try:

        st.subheader("Response")

        placeholder = st.empty()

        accumulated_text = ""

        with requests.post(
            "http://127.0.0.1:8000/generate",
            json={
                "prompt": prompt
            },
            stream=True,
            timeout=300
        ) as response:

            response.raise_for_status()

            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True
            ):
                if chunk:
                    accumulated_text += chunk
                    placeholder.markdown(accumulated_text)

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")