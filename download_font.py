import urllib.request
import zipfile
import os
import io

url = "https://fonts.google.com/download?family=Noto%20Sans%20TC"
save_path = "assets/fonts/font.ttf"
temp_zip = "assets/fonts/font.zip"

print(f"Downloading font from {url}...")
try:
    urllib.request.urlretrieve(url, temp_zip)
    print("Download complete. Extracting...")

    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        # Look for the Regular font file
        for file in zip_ref.namelist():
            if "Regular.ttf" in file or "Regular.otf" in file:
                print(f"Found font file: {file}")
                # Extract to specific path
                with zip_ref.open(file) as source, open(save_path, "wb") as target:
                    target.write(source.read())
                print(f"Font saved to {save_path}")
                break
        else:
            # If no Regular found, just take the first ttf/otf
            for file in zip_ref.namelist():
                if file.endswith(".ttf") or file.endswith(".otf"):
                    print(f"Found fallback font file: {file}")
                    with zip_ref.open(file) as source, open(save_path, "wb") as target:
                        target.write(source.read())
                    print(f"Font saved to {save_path}")
                    break

    os.remove(temp_zip)
    print("Cleanup complete.")

except Exception as e:
    print(f"Error downloading font: {e}")
