import os
from PIL import Image

projects = [
    "high-frequency-crypto-trade-simulator",
    "vantage-terminal",
    "storyline-io",
    "legalese-ai",
    "aether-glide",
    "nse-trade-simulation",
    "budgetroam"
]

base_dir = r"d:\portfolio hugo\content\project"

for project in projects:
    img_path = os.path.join(base_dir, project, "featured.png")
    if os.path.exists(img_path):
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                if width == height: # Only crop if square
                    new_height = int(width * 9 / 16)
                    top = (height - new_height) // 2
                    bottom = (height + new_height) // 2
                    crop_box = (0, top, width, bottom)
                    
                    cropped_img = img.crop(crop_box)
                    cropped_img.save(img_path)
                    print(f"Cropped {project} to {width}x{new_height}")
                else:
                    print(f"Skipping {project}: Dimensions {width}x{height} are not square.")
        except Exception as e:
            print(f"Error processing {project}: {e}")
    else:
        print(f"File not found: {img_path}")
