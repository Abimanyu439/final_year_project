from fastapi import APIRouter, UploadFile, File
from app.services.yolo_service import process_image_and_detect

router = APIRouter()

@router.post("/detect")
async def detect_vegetables(image: UploadFile = File(...)):
    image_bytes = await image.read()
    
    vegetables, confidences = process_image_and_detect(image_bytes)
    
    return {
        "vegetables": vegetables,
        "confidence": confidences
    }