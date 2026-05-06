from pydantic import BaseModel
from typing import List

# Data model for incoming request to /recommend
class RecommendRequest(BaseModel):
    vegetables: List[str]  # CHANGED 'String' to 'str'

# Data model for outgoing response from /recommend
class RecipeResponse(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]
    vegetables_required: List[str]
    youtube_link: str
    match_score: float