from fastapi import APIRouter
from app.models.schemas import RecommendRequest
from app.services.recipe_service import get_recommendations

router = APIRouter()

@router.post("/recommend")
def recommend_recipes(request: RecommendRequest):
    recommendations = get_recommendations(request.vegetables)
    return {
        "identified_ingredients": request.vegetables,
        "exact_matches": recommendations["exact_matches"],
        "further_recommendations": recommendations["further_recommendations"]
    }