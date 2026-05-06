from ultralytics import YOLO
import torch

def main():
    # Use 'n' (Nano) because 18k images provide enough detail 
    # to make even the smallest model very smart.
    model = YOLO('yolov8n.pt') 

    print("🚀 Starting High-Volume Training (18k images) on RTX 3050...")
    
    results = model.train(
        data="E:/AI_Recipe_Backend/dataset/data.yaml", 
        epochs=30,                  # 30 is plenty for 18,000 images
        imgsz=640,                  
        batch=16,                   # Nano model allows a larger batch size on 3050
        device=0,                   
        patience=5,                 # Auto-stop when it reaches peak accuracy
        name="18k_veg_model",
        workers=4                   # Use more CPU threads to feed images to GPU
    )

    print("🎉 Training Complete!")

if __name__ == '__main__':
    main()