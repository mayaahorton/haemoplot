import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Full-resolution mask generation from main analysis
def generate_masks(image_path):
    image = cv2.imread(image_path)
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l_channel, a_channel, b_channel = cv2.split(image_lab)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(a_channel, (5, 5), 0)

    # Adaptive thresholds (can be tuned further)
    # (Will eventually need replacing with a better approach)
    absorbed_thresh = np.percentile(blurred, 75)
    standing_thresh = np.percentile(blurred, 95) 

    absorbed_mask = (blurred > absorbed_thresh).astype(np.uint8)
    standing_mask = (blurred > standing_thresh).astype(np.uint8)

    return absorbed_mask, standing_mask

# Plots images with contours to identify thresholding inconsistencies 
def debug_stain_masks(image_path, absorbed_mask, standing_mask, save_path=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    absorbed_contours, _ = cv2.findContours(absorbed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    standing_contours, _ = cv2.findContours(standing_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    overlay = image_rgb.copy()
    cv2.drawContours(overlay, absorbed_contours, -1, (0, 255, 0), 2)  # Green
    cv2.drawContours(overlay, standing_contours, -1, (255, 0, 0), 2)  # Blue

    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    axs[0].imshow(image_rgb)
    axs[0].set_title("Original")
    axs[1].imshow(absorbed_mask, cmap='gray')
    axs[1].set_title("Absorbed Mask")
    axs[2].imshow(standing_mask, cmap='gray')
    axs[2].set_title("Standing Mask")
    axs[3].imshow(overlay)
    axs[3].set_title("Contour Overlay")

    for ax in axs:
        ax.axis('off')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()

# Selects the highest and lowest volume images
def get_top_and_bottom_images(csv_path, image_dir, n=5):
    df = pd.read_csv(csv_path)

    if 'total_volume' not in df.columns:
        df['total_volume'] = df['absorbed_volume'] + df['standing_volume']

    top_files = df.sort_values(by='total_volume', ascending=False).head(n)['filename'].tolist()
    bottom_files = df.sort_values(by='total_volume', ascending=True).head(n)['filename'].tolist()

    top_paths = [os.path.join(image_dir, f) for f in top_files]
    bottom_paths = [os.path.join(image_dir, f) for f in bottom_files]

    return top_paths, bottom_paths

# Get five images with highest and lowest volume and show contours
if __name__ == "__main__":
    CSV_PATH = "stain_dual_volume_summary.csv"
    IMAGE_DIR = "images"
    DEBUG_OUT = "debug"

    os.makedirs(DEBUG_OUT, exist_ok=True)

    top_imgs, bottom_imgs = get_top_and_bottom_images(CSV_PATH, IMAGE_DIR, n=5) 

    for i, img_path in enumerate(top_imgs):
        absorbed, standing = generate_masks(img_path)
        debug_stain_masks(img_path, absorbed, standing, save_path=os.path.join(DEBUG_OUT, f"top_{i}.png"))

    for i, img_path in enumerate(bottom_imgs):
        absorbed, standing = generate_masks(img_path)
        debug_stain_masks(img_path, absorbed, standing, save_path=os.path.join(DEBUG_OUT, f"bottom_{i}.png"))
