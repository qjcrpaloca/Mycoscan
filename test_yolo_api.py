import requests
import os

# Adjust host/port if your app runs elsewhere
URL = "http://127.0.0.1:5000/api/predict"

# Example image inside static uploads (change if necessary)
image_path = os.path.join("static", "uploads", "scans", "cat4.avif")

if not os.path.exists(image_path):
    print(f"Test image not found at {image_path}. Please place a JPG/PNG at that path or update the script.")
    raise SystemExit(1)

with open(image_path, 'rb') as f:
    files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
    print(f"Sending request to {URL} with {image_path}...")
    r = requests.post(URL, files=files, timeout=30)

print("Status:", r.status_code)
try:
    print(r.json())
except Exception:
    print(r.text)
