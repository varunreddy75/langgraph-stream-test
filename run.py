import threading
import subprocess
import os


def start_api():
    subprocess.run([
        "uvicorn",
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ])


def start_streamlit():
    subprocess.run([
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.address",
        "0.0.0.0",
        "--server.port",
        os.environ.get("PORT", "10000"),
        "--server.headless",
        "true"
    ])


threading.Thread(target=start_api, daemon=True).start()

start_streamlit()