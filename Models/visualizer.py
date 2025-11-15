import cv2
import numpy as np

def draw_segmentation(img, nail_mask, fungi_mask):
    # Ensure 3-channel overlay
    overlay = img.copy()
    color_mask = np.zeros_like(img, dtype=np.uint8)

    # Define colors (BGR)
    color_mask[nail_mask > 0] = (0, 255, 255)   # yellow for nail
    color_mask[fungi_mask > 0] = (0, 0, 255)    # red for fungi

    # Blend color mask with image
    blended = cv2.addWeighted(img, 1.0, color_mask, 0.4, 0)
    return blended


def draw_grid(img, bbox, rows=4, cols=5):
    """Draw OSI grid on image with thick, visible white lines"""
    x_min, y_min, x_max, y_max = bbox
    h, w = y_max - y_min, x_max - x_min
    step_y, step_x = h // rows, w // cols

    # Draw outer box with thick white line
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 255, 255), 4)

    # Draw grid lines with thick white lines for high visibility
    for i in range(1, rows):
        y = y_min + i * step_y
        cv2.line(img, (x_min, y), (x_max, y), (255, 255, 255), 3)
    for j in range(1, cols):
        x = x_min + j * step_x
        cv2.line(img, (x, y_min), (x, y_max), (255, 255, 255), 3)

    return img
