import cv2
import numpy as np
from ultralytics import YOLO

# Load model once at startup
model = YOLO('best.pt')

def process_image_and_detect(image_bytes: bytes, conf_thresh=0.45, iou_thresh=0.5):
    # 1. Preprocessing: Convert bytes to OpenCV Image (Numpy Array)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2. Prediction Pipeline (Includes Resize & Normalize internally by YOLO)
    # iou=0.5 handles Non-Max Suppression (removes overlapping duplicate boxes)
    results = model.predict(img, conf=conf_thresh, iou=iou_thresh, save=False)

    detected_vegetables = []
    confidences = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            name = model.names[class_id].lower()
            conf = float(box.conf[0])
            
            detected_vegetables.append(name)
            confidences.append(round(conf, 2))

    # Remove duplicates but keep highest confidence
    unique_vegs = list(set(detected_vegetables))
    
    return unique_vegs, confidences