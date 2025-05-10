import cv2
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# CONFIGURATION
KNOWN_WIDTH_CM = 10.0
VOLUME_PER_CM2_ABSORBED = 0.075
DEPTH_CM_STANDING = 0.1
IMAGE_FOLDER = "images"
OUTPUT_CSV = "stain_dual_volume_summary.csv"
PLOT_OUTPUT = "volume_over_time.png"

# def extract_date_from_filename(filename):
#     for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y-%m-%d_%H%M", "%d-%m-%Y"):
#         try:
#             base = os.path.basename(filename).split('.')[0]
#             date_str = ''.join(filter(lambda c: c.isdigit() or c == '-', base))
#             return datetime.strptime(date_str, fmt)
#         except ValueError:
#             continue
#     return None  # Unknown date format

def extract_date_from_filename(filename):
    """
    Extracts a datetime object from a filename in the format YYYYMMDD_HHMMSS.
    Example: '20240325_091524.jpg' -> datetime(2024, 3, 25, 9, 15, 24)
    """
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    
    try:
        date_str = name.split('_')[0] + '_' + name.split('_')[-1]
        return datetime.strptime(date_str, "%Y%m%d_%H%M%S")
    except Exception as e:
        print(f"Could not parse date from filename {filename}: {e}")
        return None

def estimate_dual_volume(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    px_per_cm = width / KNOWN_WIDTH_CM

    _, absorbed_mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    _, standing_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    absorbed_contours, _ = cv2.findContours(absorbed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    standing_contours, _ = cv2.findContours(standing_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    absorbed_pixels = sum(cv2.contourArea(c) for c in absorbed_contours)
    standing_pixels = sum(cv2.contourArea(c) for c in standing_contours)
    absorbed_only_pixels = max(0, absorbed_pixels - standing_pixels)

    absorbed_cm2 = absorbed_only_pixels / (px_per_cm ** 2)
    standing_cm2 = standing_pixels / (px_per_cm ** 2)

    absorbed_volume = absorbed_cm2 * VOLUME_PER_CM2_ABSORBED
    standing_volume = standing_cm2 * DEPTH_CM_STANDING
    total_volume = absorbed_volume + standing_volume

    return {
        "image": os.path.basename(image_path),
        "date": extract_date_from_filename(image_path),
        "absorbed_cm2": round(absorbed_cm2, 2),
        "standing_cm2": round(standing_cm2, 2),
        "absorbed_mL": round(absorbed_volume, 2),
        "standing_mL": round(standing_volume, 2),
        "total_mL": round(total_volume, 2),
    }

# Run analysis
results = []
for file in os.listdir(IMAGE_FOLDER):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(IMAGE_FOLDER, file)
        result = estimate_dual_volume(full_path)
        if result:
            results.append(result)

# Sort by date if available
results.sort(key=lambda r: r["date"] or datetime.min)

# Write CSV
with open(OUTPUT_CSV, "w", newline="") as csvfile:
    fieldnames = ["image", "date", "absorbed_cm2", "standing_cm2", "absorbed_mL", "standing_mL", "total_mL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

# Plotting
dates = [r["date"] for r in results if r["date"]]
total_volumes = [r["total_mL"] for r in results if r["date"]]
standing_volumes = [r["standing_mL"] for r in results if r["date"]]
absorbed_volumes = [r["absorbed_mL"] for r in results if r["date"]]

if dates:
    plt.figure(figsize=(10, 6))
    plt.plot(dates, total_volumes, label="Total Volume", color="red", linewidth=2)
    plt.plot(dates, standing_volumes, label="Standing (Liquid)", color="maroon", linestyle="--")
    plt.plot(dates, absorbed_volumes, label="Absorbed", color="orange", linestyle=":")
    plt.xlabel("Date")
    plt.ylabel("Volume (mL)")
    plt.title("Blood Stain Volume Over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT)
    print(f"Plot saved to '{PLOT_OUTPUT}'")

print(f"Processed {len(results)} image(s). CSV saved to '{OUTPUT_CSV}'")