import cv2
import numpy as np
from ultralytics import YOLO

class NailSegmentation:
    def __init__(self, model_path="best.pt"):
        self.model = YOLO(model_path)

    def segment(self, img):
        results = self.model.predict(img, verbose=False)[0]
        nail_mask = np.zeros(img.shape[:2], np.uint8)
        fungi_mask = np.zeros(img.shape[:2], np.uint8)
        nail_bbox = None  # will store YOLO bbox

        for box, cls, mask in zip(results.boxes.xyxy, results.boxes.cls, results.masks.data):
            label = results.names[int(cls)].lower()
            x_min, y_min, x_max, y_max = map(int, box[:4])
            mask_img = (mask.cpu().numpy() * 255).astype(np.uint8)
            mask_resized = cv2.resize(mask_img, (img.shape[1], img.shape[0]))

            if label == "nail":
                nail_mask = cv2.bitwise_or(nail_mask, mask_resized)
                nail_bbox = (x_min, y_min, x_max, y_max)
            elif label == "affected":  # YOLO model uses "affected" for fungal/infected areas
                fungi_mask = cv2.bitwise_or(fungi_mask, mask_resized)

        return nail_mask, fungi_mask, nail_bbox
