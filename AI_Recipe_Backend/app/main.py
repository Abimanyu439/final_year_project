from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from ultralytics import YOLO
import cv2
import numpy as np
import hashlib
import os
import re
from pymongo import MongoClient

# Public base URL of this backend (ngrok tunnel for localhost)
PUBLIC_BASE_URL = "https://hatbox-shindig-counting.ngrok-free.dev"

app = FastAPI()

# Allow the Android app / browsers to call us through the ngrok tunnel
app.add_middleware(
    CORSMiddleware,
    allow_origins=[PUBLIC_BASE_URL, "http://localhost", "http://127.0.0.1", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve any locally curated recipe images from /static/recipes/<slug>.jpg
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
os.makedirs(os.path.join(STATIC_DIR, "recipes"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load Model
model = YOLO('best.pt')

# MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client.ai_recipe_db
recipes_collection = db.recipes


def _slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return s or "recipe"


# Tag-to-keyword maps for building the loremflickr query.
# loremflickr serves real Flickr photos that match ALL the tags
# given (intersection). We pick exactly 3 tags — protein/main veg,
# dish type, and "food" — to get a relevant photo without making
# the query so narrow that Flickr falls back to a placeholder.
_INGREDIENT_TAGS = [
    # Compound Tamil words first so they shadow generic substrings
    # (e.g. "muttaikose" must beat "muttai", "urulaikizhangu" beats nothing
    # but is listed early for clarity).
    ("muttaikose", "cabbage"),
    ("urulaikizhangu", "potato"),
    ("vellarikkai", "cucumber"),
    ("kizhangu", "potato"),
    ("vengaya", "onion"),
    ("thakkali", "tomato"),
    ("poondu", "garlic"),
    # Citrus — kumquat is treated as lemon since both visually fit
    # the lemon-pickle / lemon-fry photo pools on Flickr.
    ("kumquat", "lemon"),
    ("lemon", "lemon"),
    # Proteins
    ("chicken", "chicken"), ("kozhi", "chicken"),
    ("fish", "fish"), ("meen", "fish"),
    ("shrimp", "shrimp"), ("prawn", "shrimp"), ("eral", "shrimp"),
    ("beef", "beef"),
    ("pork", "pork"),
    ("tofu", "tofu"), ("paneer", "tofu"),
    # Vegetables
    ("cauliflower", "cauliflower"), ("gobi", "cauliflower"),
    ("cabbage", "cabbage"),
    ("carrot", "carrot"),
    ("cucumber", "cucumber"),
    ("potato", "potato"), ("urulai", "potato"),
    ("tomato", "tomato"),
    ("garlic", "garlic"),
    ("ginger", "ginger"), ("inji", "ginger"),
    ("onion", "onion"),
    # Egg keywords last so "muttaikose" can shadow "muttai"
    ("omelette", "egg"), ("muttai", "egg"), ("egg", "egg"),
]

_DISH_TAGS = [
    ("biryani", "biryani"),
    ("rasam", "soup"),
    ("salad", "salad"), ("kosambari", "salad"),
    ("raita", "salad"), ("pachadi", "salad"),
    ("pickle", "pickle"), ("oorugai", "pickle"),
    ("rice", "rice"), ("sadam", "rice"),
    ("65", "fry"),
    ("fry", "fry"), ("varuval", "fry"), ("roast", "fry"),
    ("poriyal", "fry"), ("chukka", "fry"), ("sukka", "fry"),
    ("scramble", "fry"), ("kalaki", "fry"), ("omelette", "fry"),
    ("relish", "chutney"), ("kosu", "chutney"), ("thokku", "chutney"),
    ("kuzhambu", "curry"), ("kurma", "curry"),
    ("salna", "curry"), ("masala", "curry"), ("kootu", "curry"),
]


# Per-slug URL overrides for recipes whose auto-generated thumbnail is
# wrong. The slug is _slugify(recipe["name"]). Add an entry here when a
# specific recipe needs a curated image (or drop a JPEG at
# static/recipes/<slug>.jpg, which takes even higher priority).
_RECIPE_URL_OVERRIDES = {
    # Was returning meatballs+veggies — pin to TheMealDB Tandoori Chicken
    # (dry red roasted chicken, visually close to Tamil dry-fry style).
    "pallipalayam-chicken-fry": "https://www.themealdb.com/images/media/meals/qptpvt1487339892.jpg",
}


def _build_image_tags(recipe: dict) -> str:
    """Return a 3-tag loremflickr query string built from the recipe.

    Format: <main-ingredient>,<dish-type>,food. 3 tags is the sweet
    spot — fewer and the photos drift, more and Flickr returns the
    'no match' placeholder image. The name is scanned before the
    ingredient list so the dish's namesake (e.g. "Vengaya" = onion)
    wins over secondary ingredients.
    """
    name = (recipe.get("name") or "").lower()
    ing = " ".join(recipe.get("vegetables_required", [])
                   + recipe.get("ingredients", [])).lower()

    main = None
    for keyword, tag in _INGREDIENT_TAGS:
        if keyword in name:
            main = tag
            break
    if main is None:
        for keyword, tag in _INGREDIENT_TAGS:
            if keyword in ing:
                main = tag
                break
    if main is None:
        main = "indian"

    dish = "curry"
    for keyword, tag in _DISH_TAGS:
        if keyword in name:
            dish = tag
            break

    # "Thokku/Kosu" with a protein is a thick gravy (e.g. Eral Thokku =
    # Prawn Gravy, Muttai Thokku = Egg Masala) — visually a curry, not a
    # chutney. Re-route protein+chutney to curry so Flickr returns the
    # right pool. Veg "thokku/kosu" stays as chutney (correct visual).
    if dish == "chutney" and main in {"chicken", "fish", "shrimp",
                                       "egg", "beef", "pork"}:
        dish = "curry"

    if main == dish:
        return f"{main},indian,food"
    return f"{main},{dish},food"


def make_recipe_image_url(recipe: dict) -> str:
    """Recipe-specific thumbnail.

    1. If a locally curated image exists at static/recipes/<slug>.jpg, serve
       it via the ngrok tunnel (highest priority — drop a JPEG there to
       override the auto thumbnail for any recipe).
    2. Otherwise return a deterministic loremflickr URL whose tags are
       derived from the recipe's main ingredient and dish type. loremflickr
       returns real Flickr photos that match all tags, and the lock seed
       guarantees the same recipe maps to the same photo every time.
    """
    name = recipe.get("name", "Recipe")
    slug = _slugify(name)

    local_path = os.path.join(STATIC_DIR, "recipes", f"{slug}.jpg")
    if os.path.exists(local_path):
        return f"{PUBLIC_BASE_URL}/static/recipes/{slug}.jpg"

    if slug in _RECIPE_URL_OVERRIDES:
        return _RECIPE_URL_OVERRIDES[slug]

    tags = _build_image_tags(recipe)
    seed = int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:8], 16)
    return f"https://loremflickr.com/800/600/{tags}?lock={seed}"

class RecommendRequest(BaseModel):
    vegetables: List[str]

class JarvisRequest(BaseModel):
    text: str

@app.post("/jarvis")
def jarvis_assistant(request: JarvisRequest):
    user_text = request.text.lower()
    all_recipes = list(recipes_collection.find({}, {"_id": 0}))
    
    # Simple NLP logic
    greeting_words = ["hi", "hello", "hey", "jarvis"]
    if any(word in user_text for word in greeting_words):
        return {"response": "Hello Boss! I am Jarvis, your personal AI Chef. What ingredients do you have today?"}
        
    found_vegs = []
    # Simple keyword extraction
    for r in all_recipes:
        for veg in r.get("vegetables_required", []):
            if veg.lower() in user_text and veg.lower() not in found_vegs:
                found_vegs.append(veg.lower())
                
    if found_vegs:
        return {"response": f"I see you mentioned {', '.join(found_vegs)}. You can upload their picture, or I can suggest recipes like {all_recipes[0].get('title', 'a good dish')}."}
    
    return {"response": "I am here to help you cook! Tell me what ingredients you have."}

@app.post("/detect")
async def detect_vegetables(image: UploadFile = File(...)):
    image_bytes = await image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model.predict(img, conf=0.45, iou=0.5, agnostic_nms=True)
    
    detected = set()
    for result in results:
        for box in result.boxes:
            name = model.names[int(box.cls[0])].lower().strip()
            detected.add(name)
    
    return {"vegetables": list(detected)}

@app.post("/recommend")
def recommend_recipes(request: RecommendRequest):
    user_vegs = [v.lower().strip() for v in request.vegetables]
    all_recipes = list(recipes_collection.find({}, {"_id": 0}))

    exact_matches = []
    further_recommendations = []

    for r in all_recipes:
        # Always replace the stored imageUrl with a recipe-specific thumbnail
        r["imageUrl"] = make_recipe_image_url(r)

        req_vegs = set([v.lower().strip() for v in r.get("vegetables_required", [])])
        overlap = set(user_vegs).intersection(req_vegs)
        
        if overlap:
            score = (len(overlap) / len(req_vegs)) * 100
            if score >= 20: # 20% match threshold
                r_copy = r.copy()
                r_copy["match_score"] = round(score, 1)
                
                # Keep track of missing ingredients
                missing_vegs = list(req_vegs - set(user_vegs))
                r_copy["missing_ingredients"] = missing_vegs
                
                if len(missing_vegs) == 0:
                    exact_matches.append(r_copy)
                else:
                    further_recommendations.append(r_copy)
                
    exact_matches.sort(key=lambda x: x["match_score"], reverse=True)
    further_recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "identified_ingredients": request.vegetables,
        "exact_matches": exact_matches,
        "further_recommendations": further_recommendations
    }