import os
from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# Load your custom trained model
# If you haven't trained yet, use 'yolov8n.pt' for a general demo
model = YOLO('best.pt') 

@app.route('/detect-vegetables', methods=['POST'])
def detect_vegetables():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    # Save the file temporarily
    img_path = "temp_capture.jpg"
    file.save(img_path)

    # 1. Run Inference
    # conf=0.5 means only return items with >50% certainty
    results = model.predict(source=img_path, conf=0.5, save=False)

    detected_list = []
    confidences = []

    # 2. Parse Results
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            name = model.names[class_id]
            conf = float(box.conf[0])
            
            # Map classes to your 4 required vegetables
            detected_list.append(name.lower())
            confidences.append(round(conf, 2))

    # 3. Simple Recipe Mapping Logic
    recipe_suggestion = "Browse common recipes"
    unique_veg = set(detected_list)
    
    if "tomato" in unique_veg and "onion" in unique_veg:
        recipe_suggestion = "Tomato Onion Curry"
    elif "potato" in unique_veg and "carrot" in unique_veg:
        recipe_suggestion = "Potato Carrot Mash / Veg Fry"
    elif "tomato" in unique_veg and "potato" in unique_veg:
        recipe_suggestion = "Aloo Tamatar (Potato Tomato Gravy)"

    return jsonify({
        "detected_vegetables": list(unique_veg),
        "confidence_scores": confidences,
        "recipe_suggestion": recipe_suggestion
    })

if __name__ == '__main__':
    # Run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)