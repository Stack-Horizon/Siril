"""
================================================================================
REVISION HISTORY:
v1.0.0 (Initial)  - Added core watermarking logic using Pillow library.
v1.1.0 (Update)   - Added Tkinter pop-up for dynamic target name input.
v1.2.0 (Fix)      - Implemented automatic dependency bootloader for PIL & sirilpy.
v1.3.0 (Fix)      - Replaced .filepath with get_cwd() to resolve FFit error layers.
v1.4.0 (Fix)      - Switched to explicit IPC command sending to resolve 'get_cwd' attribute error.
v1.5.0 (Fix)      - Rewrote using siril.cmd and direct Tkinter manual fallback file selection.
v1.6.0 (Update)   - Streamlined code execution loop directly to the working manual selector.
v1.7.0 (Update)   - Replaced single prompt with an expanded custom multi-field configuration GUI.
v1.8.0 (Update)   - Restructured into a clean 3-line layout including Location and Tech Specs.
================================================================================
"""

import sys
import subprocess
import os

# 1. Automatic Dependency Check and Installer
def install_dependencies():
    required_modules = {
        "PIL": "Pillow",
        "sirilpy": "sirilpy"
    }
    
    missing_packages = []
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(package_name)
            
    if missing_packages:
        print(f"[Watermark Tool] Missing dependencies found: {missing_packages}. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("[Watermark Tool] Dependencies installed successfully!")
        except Exception as e:
            print(f"[Watermark Tool] Critical Error: Automatic installation failed: {e}")
            sys.exit(1)

install_dependencies()

# 2. Main Script Execution
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

class WatermarkDialog(tk.Toplevel):
    """Custom multi-field popup window mapped to the 3-line layout specifications."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Watermark Data Input")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.geometry("450x260")
        
        self.result = None
        self.columnconfigure(1, weight=1)
        
        # Row 0: Line 1 - Signature
        tk.Label(self, text="Line 1: Image by:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.ent_sig = tk.Entry(self)
        self.ent_sig.insert(0, "Astrophotographer")
        self.ent_sig.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        
        # Row 1: Line 2 - Target Name
        tk.Label(self, text="Line 2: Target Name:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.ent_target = tk.Entry(self)
        self.ent_target.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        
        # Row 2: Line 2 - Telescope
        tk.Label(self, text="Line 2: Telescope:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.ent_scope = tk.Entry(self)
        self.ent_scope.insert(0, "80mm Refractor")
        self.ent_scope.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        
        # Row 3: Line 2 - Location
        tk.Label(self, text="Line 2: Location:").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.ent_loc = tk.Entry(self)
        self.ent_loc.insert(0, "Backyard Observatory")
        self.ent_loc.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
        
        # Row 4: Line 3 - Camera & Filters (Or exposure details)
        tk.Label(self, text="Line 3: Camera / Tech Info:").grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.ent_tech = tk.Entry(self)
        self.ent_tech.insert(0, "ASI2600MC Pro | Optolong l-Quad Enhance Filter")
        self.ent_tech.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        
        # Action Buttons
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Apply", width=10, command=self.on_apply).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.on_cancel).pack(side="left", padx=5)
        
        # Set focus to Target box since it starts blank
        self.ent_target.focus_set()
        
    def on_apply(self):
        self.result = {
            "sig": self.ent_sig.get().strip(),
            "target": self.ent_target.get().strip(),
            "scope": self.ent_scope.get().strip(),
            "loc": self.ent_loc.get().strip(),
            "tech": self.ent_tech.get().strip()
        }
        self.destroy()
        
    def on_cancel(self):
        self.destroy()

def get_watermark_details():
    root = tk.Tk()
    root.withdraw()
    dialog = WatermarkDialog(root)
    root.wait_window(dialog)
    data = dialog.result
    root.destroy()
    return data

def select_file_manually():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        title="Please select your processed image file:",
        filetypes=[("TIFF Files", "*.tif;*.tiff"), ("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")]
    )
    root.destroy()
    return file_path

def apply_watermark():
    print("[Watermark Tool] Launching file selection window...")
    image_path = select_file_manually()

    if not image_path or not os.path.exists(image_path):
        print("[Watermark Tool] Error: No valid image file was selected or found.")
        return

    # Prompt user for all details via the 3-line layout form
    metadata = get_watermark_details()
    if not metadata or not metadata["target"]:
        print("[Watermark Tool] Cancelled: Form incomplete or target missing.")
        return

    # Set up text lines based on user prompt mapping
    line1_text = f"Image by: {metadata['sig']}"
    line2_text = f"{metadata['target']} | Telescope: {metadata['scope']} | Location: {metadata['loc']}"
    line3_text = metadata["tech"]

    # Setup file output naming structures
    dir_name, file_name = os.path.split(image_path)
    base_name, ext = os.path.splitext(file_name)
    output_path = os.path.join(dir_name, f"{base_name}_watermarked{ext}")

    # Process and blend the watermark canvas layers
    base = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
    
    # Fonts
    font_header = ImageFont.truetype("arial.ttf", 60)
    font_sublines = ImageFont.truetype("arial.ttf", 30)
    
    draw = ImageDraw.Draw(txt_layer)
    margin = 50
    
    # Bottom up line position spacing calculations
    line3_pos = (margin, base.height - margin - 40)
    line2_pos = (margin, base.height - margin - 90)
    line1_pos = (margin, base.height - margin - 170)
    
    # Blending the text elements into the canvas
    draw.text(line1_pos, line1_text, font=font_header, fill=(255, 255, 255, 140)) # Slightly bolder alpha
    draw.text(line2_pos, line2_text, font=font_sublines, fill=(210, 210, 210, 115))
    draw.text(line3_pos, line3_text, font=font_sublines, fill=(210, 210, 210, 115))
    
    # Merge layers
    watermarked = Image.alpha_composite(base, txt_layer)
    final_image = watermarked.convert("RGB")
    
    fmt = "JPEG" if ext.lower() in [".jpg", ".jpeg"] else "TIFF"
    final_image.save(output_path, fmt)
    
    print(f"[Watermark Tool] Success! Saved to: {output_path}")

if __name__ == "__main__":
    apply_watermark()
