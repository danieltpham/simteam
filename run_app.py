import uvicorn
import subprocess
import threading
import time


def run_fastapi():
    uvicorn.run("simteam.server.router:app", host="0.0.0.0", port=10000, reload=False)


def run_streamlit():
    subprocess.run([
        "streamlit", "run", "simteam/ui/main.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ],
        check=True)


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    time.sleep(1)
    run_streamlit()
