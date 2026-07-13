import os
import glob
import tkinter as tk
from tkinter import filedialog

def get_base_directory_from_file():
    """Opens a native desktop popup to pick the starting directory folder directly."""
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    
    print("\n[UI] Opening Folder Browser... Choose your base imaging folder.")
    # FIXED: Replaced file picker with direct folder directory picker
    selected_dir = filedialog.askdirectory(
        title="Select your starting/base astrophotography directory folder"
    )
    root.destroy()
    
    if not selected_dir:
        return None
    return os.path.abspath(selected_dir)

def scan_for_pairs(base_dir):
    """Deep-crawls downstream directories using wildcards to match imaging pairs."""
    valid_pairs = []
    extensions = ('*.fit', '*.fits', '*.fits', '*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg', '*.FIT', '*.FITS')

    for root_dir, _, _ in os.walk(base_dir):
        folder_short = os.path.basename(root_dir)
        if folder_short:
            print(f"  -> Crawling folder: {folder_short}")
            
        starless_files = []
        starmask_files = []
        
        for ext in extensions:
            starless_files.extend(glob.glob(os.path.join(root_dir, f"*starless*{ext}")))
            starmask_files.extend(glob.glob(os.path.join(root_dir, f"*star_mask*{ext}")))
            starmask_files.extend(glob.glob(os.path.join(root_dir, f"*starmask*{ext}")))

        starless_files = list(set(starless_files))
        starmask_files = list(set(starmask_files))

        if starless_files and starmask_files:
            valid_pairs.append({
                'folder': os.path.basename(root_dir),
                'starless': starless_files[0], # Extract the first valid matching path string
                'starmask': starmask_files[0], # Extract the first valid matching path string
                'output_dir': root_dir
            })
            
    return valid_pairs
