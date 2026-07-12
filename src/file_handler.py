import os
import glob
import tkinter as tk
from tkinter import filedialog

def get_base_directory():
    """Opens a native file browser window and extracts its parent directory path."""
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    
    print("\n[UI] Opening Browser... Choose ANY file inside your target galaxy directory.")
    selected_file = filedialog.askopenfilename(
        title="Click ANY file inside your main imaging folder to set the scan base",
        filetypes=[("All Files", "*.*")]
    )
    root.destroy()
    
    if not selected_file:
        return None
    return os.path.dirname(os.path.abspath(selected_file))

def scan_for_pairs(base_dir):
    """Deep-crawls downstream directories using wildcards to match imaging pairs."""
    valid_pairs = []
    extensions = ('*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg', '*.fit', '*.fits', '*.FIT', '*.FITS')

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
            # Safely grab the first matched string file paths from the list elements
            valid_pairs.append({
                'folder': os.path.basename(root_dir),
                'starless': starless_files[0], 
                'starmask': starmask_files[0],
                'output_dir': root_dir
            })
            
    return valid_pairs
