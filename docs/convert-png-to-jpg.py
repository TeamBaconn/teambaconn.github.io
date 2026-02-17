import os
from PIL import Image

def convert_png_to_jpg(root_dir, quality=85, delete_original=True):
    for root, dirs, files in os.walk(root_dir):
        # skip current folder → only subfolders
        if root == root_dir:
            continue

        for file in files:
            if not file.lower().endswith(".png"):
                continue

            png_path = os.path.join(root, file)
            jpg_path = os.path.join(root, os.path.splitext(file)[0] + ".jpg")

            try:
                with Image.open(png_path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    img.save(jpg_path, "JPEG", quality=quality, optimize=True)

                if delete_original:
                    os.remove(png_path)

                print(f"OK  {png_path} -> {jpg_path}")

            except Exception as e:
                print(f"FAIL {png_path} | {e}")


if __name__ == "__main__":
    ROOT_DIRECTORY = r"./"  # change if needed
    convert_png_to_jpg(ROOT_DIRECTORY, quality=85, delete_original=True)
