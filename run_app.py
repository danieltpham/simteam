import uvicorn
import subprocess
import threading
import time


def run_fastapi():
    uvicorn.run("simteam.server.router:app", host="127.0.0.1", port=10000, reload=False)


def run_streamlit():
    # Runs: streamlit run simteam/ui/main.py --server.port 8501
    subprocess.run(
        ["streamlit", "run", "simteam/ui/main.py", "--server.port", "8501"],
        check=True,
    )


if __name__ == "__main__":
    # Run FastAPI in a background thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Give FastAPI a moment to start
    time.sleep(1)

    # Run Streamlit (blocking call)
    run_streamlit()
