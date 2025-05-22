import os
import subprocess
import threading
import time
import webbrowser
import ngrok
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_uvicorn():
    """Run the FastAPI server with uvicorn."""
    print("Starting FastAPI server...")
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
    subprocess.run(["python3", "-m", "uvicorn", "main:app", "--host", "localhost", "--port", "8000"])

def run_ngrok():
    """Run ngrok to expose the FastAPI server to the internet."""
    print("Starting ngrok tunnel...")
    # Wait for uvicorn to start
    time.sleep(2)
    
    # Check if ngrok token is set
    if not os.environ.get("NGROK_AUTHTOKEN"):
        print("ERROR: NGROK_AUTHTOKEN not set!")
        print("Please set your ngrok authtoken with:")
        print("export NGROK_AUTHTOKEN=your_token_here")
        print("Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken")
        return
    
    # Start ngrok tunnel
    try:
        listener = ngrok.connect(8000, authtoken_from_env=True)
        print(f"Public URL: {listener.url()}")
        
        # Open URL in browser
        webbrowser.open(listener.url())
        
        # Keep the tunnel open
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Closing ngrok tunnel...")
            ngrok.disconnect(listener.url())
    except Exception as e:
        print(f"Error connecting to ngrok: {e}")
        print("Please check your authtoken and internet connection.")

if __name__ == "__main__":
    # Start uvicorn in a separate thread
    uvicorn_thread = threading.Thread(target=run_uvicorn)
    uvicorn_thread.daemon = True
    uvicorn_thread.start()
    
    # Start ngrok in the main thread
    run_ngrok() 