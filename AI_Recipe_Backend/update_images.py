import re
import random

images = {
    "chicken": [
        "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1626779430155-27aeb9e1fb56?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1563379926898-05f4575a4476?auto=format&fit=crop&w=800&q=80"
    ],
    "beef": [
        "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1544025162-811cba1714fc?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1574484284002-952d92456975?auto=format&fit=crop&w=800&q=80"
    ],
    "pork": [
        "https://images.unsplash.com/photo-1624933391986-778848db421a?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1563379926898-05f4575a4476?auto=format&fit=crop&w=800&q=80"
    ],
    "fish": [
        "https://images.unsplash.com/photo-1610729739502-3fe43ab03cb2?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1599084924616-e9b0183354f9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1580476262798-b9030affcd58?auto=format&fit=crop&w=800&q=80"
    ],
    "shrimp": [
        "https://images.unsplash.com/photo-1625943555419-56a2cb596640?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1559742811-822873691fc8?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1565557612660-84a1e0b57e75?auto=format&fit=crop&w=800&q=80"
    ],
    "egg": [
        "https://images.unsplash.com/photo-1614398751058-eb2e0bf63e53?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80"
    ],
    "biryani": [
        "https://images.unsplash.com/photo-1633383718081-22ac643dcd75?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1589302168068-964664d93cb0?auto=format&fit=crop&w=800&q=80"
    ],
    "veg": [
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1555126634-ae231a47df6f?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1588667500508-b1dc71be1d6d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80"
    ],
    "default": [
        "https://images.unsplash.com/photo-1495521821757-a1efb6729352?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=80"
    ]
}

# Add a little cycling counter so we don't pick identically if we can help it
counters = {k: 0 for k in images.keys()}

def get_image(name, req_vegs):
    text = (name.lower() + " " + " ".join(req_vegs).lower())
    cat = "default"
    
    if "biryani" in text:
        cat = "biryani"
    elif "chicken" in text or "kozhi" in text:
        cat = "chicken"
    elif "beef" in text:
        cat = "beef"
    elif "pork" in text:
        cat = "pork"
    elif "fish" in text or "meen" in text:
        cat = "fish"
    elif "shrimp" in text or "eral" in text or "prawn" in text:
        cat = "shrimp"
    elif "egg" in text or "muttai" in text:
        cat = "egg"
    else:
        cat = "veg"
        
    c = counters[cat]
    img = images[cat][c % len(images[cat])]
    counters[cat] += 1
    return f'"{img}"'

with open("E:/recipeee/AI_Recipe_Backend/seed_db.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
current_name = ""
current_vegs = []

for line in lines:
    name_match = re.search(r'"name":\s*"([^"]+)"', line)
    if name_match:
        current_name = name_match.group(1)
        
    veg_match = re.search(r'"vegetables_required":\s*\[(.*?)\]', line)
    if veg_match:
        current_vegs = [v.strip().strip('"').strip("'") for v in veg_match.group(1).split(",")]
        
    if '"imageUrl":' in line:
        new_url = get_image(current_name, current_vegs)
        line = re.sub(r'"imageUrl":\s*"[^"]+"', f'"imageUrl": {new_url}', line)
        
    new_lines.append(line)

with open("E:/recipeee/AI_Recipe_Backend/seed_db.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Images replaced completely.")