import tkinter as tk
from tkinter import PhotoImage
import threading
import time
import requests
import os

# --- Configuration ---
# Path to your custom image (e.g., a PNG or GIF)
# Put an image file (e.g., 'loading_mai.png') directly in your ~/bot/ directory
IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "laoding_mai.png") 

# Default Rasa server URL (adjust if yours is different)
RASA_SERVER_URL = "http://localhost:5005/status"

# How often to check Rasa status (in seconds)
CHECK_INTERVAL = 1

# --- GUI Setup ---
def create_loading_screen():
    root = tk.Tk()
    root.title("Loading Mai...")
    root.attributes('-topmost', True) # Keep window on top
    root.resizable(False, False)
    root.overrideredirect(True) # Remove window borders/title bar

    # Optional: Set window size
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Try to load image
    try:
        global img # Keep a reference to prevent garbage collection
        img = PhotoImage(file=IMAGE_PATH)
        label = tk.Label(root, image=img, bg='white')
        label.pack(expand=True, fill='both')
    except Exception as e:
        # Fallback to text if image fails
        print(f"Warning: Could not load image at {IMAGE_PATH}. Error: {e}")
        label = tk.Label(root, text="Loading Mai...\nPlease wait...", font=("Helvetica", 16), bg='white')
        label.pack(expand=True, fill='both')

    root.update_idletasks()
    root.update()
    return root

# --- Rasa Status Check ---
def check_rasa_status(root):
    while True:
        try:
            response = requests.get(RASA_SERVER_URL, timeout=0.5)
            if response.status_code == 200 and response.json().get("status") == "healthy":
                print("Rasa server is ready!")
                root.destroy() # Close the loading screen
                return
        except requests.exceptions.ConnectionError:
            pass # Rasa not up yet or connection refused
        except Exception as e:
            print(f"Error checking Rasa status: {e}")

        time.sleep(CHECK_INTERVAL)

# --- Main Execution ---
if __name__ == "__main__":
    loading_window = create_loading_screen()

    # Start checking Rasa status in a separate thread to keep GUI responsive
    status_thread = threading.Thread(target=check_rasa_status, args=(loading_window,))
    status_thread.daemon = True # Allow main program to exit even if thread is running
    status_thread.start()

    loading_window.mainloop() # Start the GUI event loop
    print("Loading screen closed.")