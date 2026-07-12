import sys
import os
from file_handler import get_base_directory_from_file, scan_for_pairs
from video_engine import render_spaceflight

def main():
    base_dir = get_base_directory_from_file()
    if not base_dir:
        print("Selection cancelled. Exiting.")
        return
        
    print(f"\nBase Directory Isolated: {base_dir}")
    print("[Step 1] Scanning downstream directories for Starless & Starmask pairs...")
    
    valid_pairs = scan_for_pairs(base_dir)

    if not valid_pairs:
        print("\n❌ No matching *starless* and *starmask* pairs found downstream.")
        return

    print("\n[Step 2] Scanning Complete. Found the following target image pairs:")
    for index, pair in enumerate(valid_pairs, 1):
        print(f"  [{index}] Folder: {pair['folder']}")
        print(f"      ↳ Starless: {os.path.basename(pair['starless'][0]) if isinstance(pair['starless'], list) else os.path.basename(pair['starless'])}")
        print(f"      ↳ Starmask: {os.path.basename(pair['starmask'][0]) if isinstance(pair['starmask'], list) else os.path.basename(pair['starmask'])}")
        print("-" * 60)

    while True:
        try:
            choice = input(f"\nSelect which image pair to animate (1 to {len(valid_pairs)}): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(valid_pairs):
                selected_pair = valid_pairs[choice_idx]
                # Standardize to pick the first matched path if it returned a wildcard list
                if isinstance(selected_pair['starless'], list):
                    selected_pair['starless'] = selected_pair['starless'][0]
                if isinstance(selected_pair['starmask'], list):
                    selected_pair['starmask'] = selected_pair['starmask'][0]
                break
            print("Invalid choice. Please pick a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

    render_spaceflight(selected_pair)

if __name__ == "__main__":
    main()
