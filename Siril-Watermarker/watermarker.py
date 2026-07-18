import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

CACHE_FILE = os.path.join(os.path.dirname(__file__), "watermark_cache.json")

def load_cached_data():
    """Retrieves saved configurations from the local JSON storage file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data_to_cache(name_data):
    """Writes the current working signature data directly to local disk."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"saved_name": name_data}, f)
    except Exception as e:
        print(f"Error updating local configuration cache: {e}")

def clear_cache_file():
    """Removes the persistent local settings block from the workspace environment."""
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
        except Exception as e:
            print(f"Error removing cached file asset: {e}")

def get_watermark_identity():
    """Manages the UI lifecycle for caching, resetting, and purging workspace metadata."""
    # Hide root window to isolate the standalone dialog popups cleanly
    root = tk.Tk()
    root.withdraw()
    
    cache = load_cached_data()
    cached_name = cache.get("saved_name", "")
    
    if cached_name:
        # Prompt the user with choices regarding existing cached data
        choice_box = tk.Toplevel(root)
        choice_box.title("Watermark Configuration Setup")
        choice_box.geometry("420x150")
        choice_box.attributes("-topmost", True)
        
        label = tk.Label(choice_box, text=f"Found existing profile: '{cached_name}'\nChoose workspace behavior:", padx=10, pady=10)
        label.pack()
        
        selection = {"action": "use"}
        
        def handle_action(act):
            selection["action"] = act
            choice_box.destroy()
            
        btn_frame = tk.Frame(choice_box)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Keep & Save", width=12, command=lambda: handle_action("use")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Reset / Modify", width=12, command=lambda: handle_action("reset")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Clear Profile", width=12, command=lambda: handle_action("clear")).grid(row=0, column=2, padx=5)
        
        choice_box.wait_window()
        
        if selection["action"] == "use":
            return cached_name
        elif selection["action"] == "clear":
            clear_cache_file()
            cached_name = ""
            # Fallthrough to ask for a new name definition below
            
    # Solicit fresh input if cache is blank or reset was requested
    user_input = simpledialog.askstring("Watermark Tool Initializer", "Enter signature text (e.g. © 2026 Stack-Horizon):")
    
    if user_input:
        # Confirm with user whether this string should be cached locally
        should_cache = messagebox.askyesno("Cache Manager", "Would you like to preserve this profile context for future automation runs?")
        if should_cache:
            save_data_to_cache(user_input)
        return user_input
        
    return "© Default Watermark Context"

# Example execution within your setup framework
if __name__ == "__main__":
    signature_text = get_watermark_identity()
    print(f"Active processing identity assigned: {signature_text}")
