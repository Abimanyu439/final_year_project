import hashlib
import os
import re

from app.utils.database import recipes_collection

# Public base URL of this backend (ngrok tunnel for localhost)
PUBLIC_BASE_URL = "https://hatbox-shindig-counting.ngrok-free.dev"

STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "static"
)

_INGREDIENT_TAGS = [
    # Compound Tamil words first so they shadow generic substrings
    ("muttaikose", "cabbage"),
    ("urulaikizhangu", "potato"),
    ("vellarikkai", "cucumber"),
    ("kizhangu", "potato"),
    ("vengaya", "onion"),
    ("thakkali", "tomato"),
    ("poondu", "garlic"),
    ("kumquat", "lemon"),
    ("lemon", "lemon"),
    ("chicken", "chicken"), ("kozhi", "chicken"),
    ("fish", "fish"), ("meen", "fish"),
    ("shrimp", "shrimp"), ("prawn", "shrimp"), ("eral", "shrimp"),
    ("beef", "beef"),
    ("pork", "pork"),
    ("tofu", "tofu"), ("paneer", "tofu"),
    ("cauliflower", "cauliflower"), ("gobi", "cauliflower"),
    ("cabbage", "cabbage"),
    ("carrot", "carrot"),
    ("cucumber", "cucumber"),
    ("potato", "potato"), ("urulai", "potato"),
    ("tomato", "tomato"),
    ("garlic", "garlic"),
    ("ginger", "ginger"), ("inji", "ginger"),
    ("onion", "onion"),
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
    "pallipalayam-chicken-fry": "https://www.themealdb.com/images/media/meals/qptpvt1487339892.jpg",
}


def _slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return s or "recipe"


def _build_image_tags(recipe: dict) -> str:
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

    # Protein "thokku/kosu" is a thick gravy (visually a curry), not a
    # chutney. Veg thokku/kosu stays a chutney (correct visual).
    if dish == "chutney" and main in {"chicken", "fish", "shrimp",
                                       "egg", "beef", "pork"}:
        dish = "curry"

    if main == dish:
        return f"{main},indian,food"
    return f"{main},{dish},food"


def make_recipe_image_url(recipe: dict) -> str:
    """Recipe-specific thumbnail. Prefers a local image at
    static/recipes/<slug>.jpg, otherwise builds a deterministic
    loremflickr URL whose tags are derived from the recipe's main
    ingredient and dish type. Same recipe -> same photo every time.
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


def get_recommendations(user_vegetables: list):
    user_set = set([v.lower() for v in user_vegetables])
    all_recipes = list(recipes_collection.find({}, {"_id": 0})) # Fetch all, omit ID

    exact_matches = []
    further_recommendations = []

    for recipe in all_recipes:
        # Always override stored imageUrl with a recipe-specific thumbnail
        recipe["imageUrl"] = make_recipe_image_url(recipe)

        req_set = set([v.lower() for v in recipe.get("vegetables_required", [])])

        # Calculate intersection (Partial Match Support)
        matched_vegs = user_set.intersection(req_set)
        match_count = len(matched_vegs)

        if match_count > 0:
            # Score formula: (Matched / Total Required) * 100
            score = (match_count / len(req_set)) * 100

            recipe["match_score"] = round(score, 1)

            # Keep track of missing ingredients
            missing_vegs = list(req_set - user_set)
            recipe["missing_ingredients"] = missing_vegs
            
            if len(missing_vegs) == 0:
                exact_matches.append(recipe)
            else:
                further_recommendations.append(recipe)
            
    # Sort by highest match score descending
    exact_matches.sort(key=lambda x: x["match_score"], reverse=True)
    further_recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "exact_matches": exact_matches,
        "further_recommendations": further_recommendations
    }