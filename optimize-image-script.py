import os
from PIL import Image

# Folders to scan
folders = [
    "static/plugin",
    "static/portfolio",
    "static/posts"
]

for folder in folders:
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".png"):
                png_path = os.path.join(root, file)
                jpg_path = os.path.splitext(png_path)[0] + ".jpg"

                try:
                    with Image.open(png_path) as img:
                        # Convert PNG → JPG (remove alpha channel)
                        rgb_img = img.convert("RGB")
                        rgb_img.save(jpg_path, "JPEG", quality=95)

                    # Remove original PNG after successful conversion
                    os.remove(png_path)
                    print(f"Converted and deleted: {png_path}")
                except Exception as e:
                    print(f"❌ Failed to convert {png_path}: {e}")