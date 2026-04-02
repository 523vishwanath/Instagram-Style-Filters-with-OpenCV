"""
Instagram-Style Filters using OpenCV
=====================================
Implements two image filters:
  1. Pencil Sketch Filter  - grayscale edge-based sketch effect
  2. Cartoon Filter        - color image with bold outlined edges
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

imagePath = "trump.jpg"          # <-- Change this to your image filename
OUTPUT_DIR = "images"            # Folder where results will be saved
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Filter 1: Pencil Sketch
# ---------------------------------------------------------------------------

def pencilSketch(image):
    """
    Converts a color (or grayscale) image into a pencil sketch.

    Steps:
      1. Convert to grayscale (if needed)
      2. Apply Gaussian Blur to reduce noise
      3. Apply Adaptive Thresholding to extract edges as a sketch

    Parameters
    ----------
    image : np.ndarray
        Input image (BGR or grayscale).

    Returns
    -------
    sketch : np.ndarray
        Binary sketch image (H x W), dtype uint8.
    """
    # Step 1: Grayscale conversion
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Step 2: Smooth to reduce noise before edge detection
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Step 3: Adaptive threshold — highlights edges like pencil strokes
    sketch = cv2.adaptiveThreshold(
        blur,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=5,
        C=2
    )

    return sketch


# ---------------------------------------------------------------------------
# Filter 2: Cartoon
# ---------------------------------------------------------------------------

def cartoonify(image):
    """
    Produces a cartoon-style version of the input image.

    Uses the pencil sketch as an edge mask — pixels not on an edge
    are set to black, keeping only the outlined regions in color.

    Parameters
    ----------
    image : np.ndarray
        Input BGR color image.

    Returns
    -------
    cartoon : np.ndarray
        Cartoon-filtered image (BGR), same shape as input.
    """
    # Get the edge mask from the sketch filter
    edgeMask = pencilSketch(image)

    # Copy the original color image
    cartoon = image.copy()

    # Zero out pixels that are NOT part of an edge
    cartoon[edgeMask != 255] = (0, 0, 0)

    return cartoon


# ---------------------------------------------------------------------------
# Main — Load, Process, Display, Save
# ---------------------------------------------------------------------------

def main():
    # Load image
    image = cv2.imread(imagePath)
    if image is None:
        raise FileNotFoundError(f"Could not load image at: '{imagePath}'")

    print(f"Loaded image — shape: {image.shape}")

    # Apply filters
    sketchResult  = pencilSketch(image)
    cartoonResult = cartoonify(image)

    print(f"Pencil sketch shape : {sketchResult.shape}")
    print(f"Cartoon image shape : {cartoonResult.shape}")

    # ---- Save outputs -------------------------------------------------------
    originalSavePath = os.path.join(OUTPUT_DIR, "original.jpg")
    sketchSavePath   = os.path.join(OUTPUT_DIR, "pencil_sketch.jpg")
    cartoonSavePath  = os.path.join(OUTPUT_DIR, "cartoon.jpg")

    cv2.imwrite(originalSavePath, image)
    cv2.imwrite(sketchSavePath,   sketchResult)
    cv2.imwrite(cartoonSavePath,  cartoonResult)

    print(f"\nSaved outputs to '{OUTPUT_DIR}/':")
    print(f"  {originalSavePath}")
    print(f"  {sketchSavePath}")
    print(f"  {cartoonSavePath}")

    # ---- Display side-by-side -----------------------------------------------
    plt.figure(figsize=(20, 8))

    plt.subplot(1, 3, 1)
    plt.imshow(image[:, :, ::-1])   # BGR -> RGB for matplotlib
    plt.title("Original", fontsize=16)
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(sketchResult, cmap="gray")
    plt.title("Pencil Sketch", fontsize=16)
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(cartoonResult[:, :, ::-1])
    plt.title("Cartoon Filter", fontsize=16)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison.png"), dpi=150)
    plt.show()
    print("Comparison plot saved.")


if __name__ == "__main__":
    main()
