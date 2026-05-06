from pymongo import MongoClient
import urllib.parse

# 1. Connect to MongoDB
try:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client.ai_recipe_db
    recipes_collection = db.recipes

    # 2. Clear old data
    recipes_collection.delete_many({})

    # Helper function to create a reliable YouTube Search URL
    def create_yt_link(query):
        base_url = "https://www.youtube.com/results?search_query="
        return base_url + urllib.parse.quote(query)

    # 3. 30+ Tamil Nadu Style Recipe Data based on YOLO classes
    real_recipes = [
        {
            "name": "Chettinad Chicken Curry",
            "ingredients": ["1/2 kg Chicken", "2 Tomatoes", "2 Onions", "Ginger", "Garlic", "Lemon juice"],
            "steps": ["Marinate chicken with turmeric and lemon.", "Sauté onions, ginger, and garlic until golden.", "Add crushed tomatoes and spices, cook until mushy.", "Add chicken, cover, and cook until tender."],
            "vegetables_required": ["chicken", "tomato", "onion", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80",
            "time": "45 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Chettinad Chicken Curry recipe in Tamil")
        },
        {
            "name": "Pallipalayam Chicken Fry",
            "ingredients": ["500g Chicken", "Small Pepper", "Onion", "Garlic"],
            "steps": ["Dry roast small peppers and grind.", "Sauté chopped onions and crushed garlic in sesame oil.", "Add the ground pepper and chicken pieces.", "Stir fry without water until the chicken cooks in its own juices."],
            "vegetables_required": ["chicken", "onion", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1626779430155-27aeb9e1fb56?auto=format&fit=crop&w=800&q=80",
            "time": "35 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Pallipalayam Chicken recipe in Tamil")
        },
        {
            "name": "Tamil Nadu Style Meen Kuzhambu (Fish Curry)",
            "ingredients": ["500g Fish", "2 Tomatoes", "Onions", "Garlic", "Tamarind Extract (optional)"],
            "steps": ["Heat gingelly oil, temper with mustard and fenugreek seeds.", "Sauté generously chopped onions and garlic cloves.", "Add chopped tomatoes and cook until oil separates.", "Add water, spices, boil, then drop the fish pieces. Cook for 10 mins."],
            "vegetables_required": ["fish", "tomato", "onion", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1610729739502-3fe43ab03cb2?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Meen Kuzhambu Fish Curry recipe in Tamil")
        },
        {
            "name": "Madurai Meen Varuval (Spicy Fish Fry)",
            "ingredients": ["500g Fish", "Lemon Juice", "Ginger Garlic Paste"],
            "steps": ["Clean the fish slices.", "Mix ginger, garlic, chilli powder, salt, and lemon juice into a thick paste.", "Coat the fish evenly and marinate for 30 mins.", "Shallow fry in oil until crispy on both sides."],
            "vegetables_required": ["fish", "lemon", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1599084924616-e9b0183354f9?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Madurai Meen Varuval Spicy Fish Fry recipe in Tamil")
        },
        {
            "name": "Eral Thokku (Prawn Gravy)",
            "ingredients": ["300g Shrimp", "2 Onions", "2 Tomatoes", "Garlic", "Ginger"],
            "steps": ["Clean and devein shrimp.", "Sauté chopped onions, crushed ginger, and garlic.", "Add diced tomatoes, cook until mushy.", "Add shrimp and cook for 8-10 minutes. Garnish with coriander."],
            "vegetables_required": ["shrimp", "onion", "tomato", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1625943555419-56a2cb596640?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Eral Thokku Prawn recipe in Tamil")
        },
        {
            "name": "Prawn Milagu Varuval (Shrimp Pepper Fry)",
            "ingredients": ["300g Shrimp", "Small Pepper", "Onion", "Garlic"],
            "steps": ["Sauté onions and garlic in a pan.", "Toss in the shrimp and stir-fry for 5 minutes.", "Crush the small fresh pepper and mix generously.", "Roast until dry and spicy."],
            "vegetables_required": ["shrimp", "onion", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1559742811-822873691fc8?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Eral Milagu Varuval Pepper Fry recipe in Tamil")
        },
        {
            "name": "Muttai Thokku (Egg Masala)",
            "ingredients": ["4 Boiled Eggs", "2 Onions", "2 Tomatoes", "Garlic"],
            "steps": ["Boil eggs, peel and make small slits.", "Sauté finely chopped onions and crushed garlic.", "Add chopped tomatoes and cook until oil separates.", "Drop in the boiled eggs and coat with the spicy tomato masala."],
            "vegetables_required": ["egg", "onion", "tomato", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1614398751058-eb2e0bf63e53?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Muttai Thokku Egg Masala recipe in Tamil")
        },
        {
            "name": "Kodaikanal Pork Roast",
            "ingredients": ["500g Pork", "Small Pepper", "Onion", "Ginger", "Garlic"],
            "steps": ["Pressure cook pork pieces with salt and turmeric.", "Sauté onions, ginger, and garlic in a pan until golden.", "Add the cooked pork and crushed small peppers.", "Roast slowly until the meat turns dark brown and slightly crispy."],
            "vegetables_required": ["pork", "onion", "ginger", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1624933391986-778848db421a?auto=format&fit=crop&w=800&q=80",
            "time": "50 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Pork Roast pepper recipe in Tamil")
        },
        {
            "name": "Coimbatore Pork Curry",
            "ingredients": ["500g Pork", "Tomato", "Onion", "Garlic", "Ginger"],
            "steps": ["Make a paste of ginger and garlic.", "Sauté onions and tomatoes into a deep gravy base.", "Add the pork pieces and mix with local spices.", "Pressure cook for 4-5 whistles until very tender."],
            "vegetables_required": ["pork", "tomato", "onion", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1563379926898-05f4575a4476?auto=format&fit=crop&w=800&q=80",
            "time": "60 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Pork Kuzhambu recipe in Tamil")
        },
        {
            "name": "Beef Chukka Varuval",
            "ingredients": ["500g Beef", "Onion", "Ginger", "Garlic", "Small Pepper"],
            "steps": ["Pressure cook beef with ginger, garlic, and salt for 6 whistles.", "In an iron tawa, sauté finely chopped onions.", "Add the cooked beef and lots of crushed pepper.", "Continually roast on low flame until dark and dry."],
            "vegetables_required": ["beef", "onion", "ginger", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&w=800&q=80",
            "time": "50 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Beef Chukka Varuval recipe in Tamil")
        },
        {
            "name": "Beef Masala Curry",
            "ingredients": ["500g Beef", "Tomato", "Onion", "Ginger", "Garlic"],
            "steps": ["Clean and boil the beef chunks.", "Fry onions, ginger, and garlic to form a thick brown paste.", "Add mashed tomatoes, ground coconut, and cooked beef.", "Simmer until the gravy thickens heavily."],
            "vegetables_required": ["beef", "tomato", "onion", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1544025162-811cba1714fc?auto=format&fit=crop&w=800&q=80",
            "time": "60 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Beef Masala Curry recipe in Tamil")
        },
        {
            "name": "Urulaikizhangu Varuval (Potato Fry)",
            "ingredients": ["3 Potatoes", "Garlic", "Onion"],
            "steps": ["Boil and peel potatoes, then dice them.", "Heat oil, temper mustard seeds, and add crushed garlic.", "Add chopped onions and sauté.", "Add potatoes and chili powder, roast until golden crust forms."],
            "vegetables_required": ["potato", "garlic", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1626779430155-27aeb9e1fb56?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Urulaikizhangu Varuval Potato Fry recipe in Tamil")
        },
        {
            "name": "Urulaikizhangu Kurma",
            "ingredients": ["2 Potatoes", "1 Tomato", "1 Onion", "Ginger Garlic Paste"],
            "steps": ["Sauté onions, tomatoes, and ginger-garlic paste.", "Add diced potatoes and water, cooking until half soft.", "Add coconut paste and simmer until creamy."],
            "vegetables_required": ["potato", "tomato", "onion", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Potato Kurma Recipe for Chapathi in Tamil")
        },
        {
            "name": "Tirunelveli Gobi Roast (Cauliflower Fry)",
            "ingredients": ["1 Cauliflower", "Ginger", "Garlic", "Lemon"],
            "steps": ["Blanch cauliflower florets in hot water.", "Make a batter using ginger-garlic paste, spices, and lemon juice.", "Coat the florets well.", "Deep fry or tawa roast until crispy."],
            "vegetables_required": ["cauliflower", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Cauliflower 65 Gobi Roast recipe in Tamil")
        },
        {
            "name": "Cauliflower Pattani Kurma",
            "ingredients": ["Cauliflower", "Tomato", "Onion", "Garlic", "Ginger"],
            "steps": ["Clean cauliflower in hot water.", "Fry onions, tomatoes, and ginger-garlic to extract oil.", "Add the cauliflower (and peas if available).", "Pour in coconut milk and boil till the cauliflower runs soft."],
            "vegetables_required": ["cauliflower", "tomato", "onion", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1555126634-ae231a47df6f?auto=format&fit=crop&w=800&q=80",
            "time": "35 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Cauliflower Kurma recipe in Tamil")
        },
        {
            "name": "Muttai Poriyal (Egg Scramble)",
            "ingredients": ["3 Eggs", "Onion", "Small Pepper", "Carrot (optional)"],
            "steps": ["Finely chop onions, pepper, and grate a little carrot.", "Sauté everything in a pan until onions turn transparent.", "Crack the eggs into the pan.", "Scramble quickly on medium heat until fully cooked."],
            "vegetables_required": ["egg", "onion", "small_pepper", "carrot"],
            "imageUrl": "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=800&q=80",
            "time": "10 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Muttai Poriyal Egg Scramble recipe in Tamil")
        },
        {
            "name": "Muttai Omelette TN Style",
            "ingredients": ["2 Eggs", "Onion", "Tomato", "Small Pepper"],
            "steps": ["Beat the eggs in a bowl.", "Mix aggressively with extremely fine chopped onions, tomatoes, and pepper.", "Pour onto a hot iron dosa tawa.", "Flip once golden brown and serve hot."],
            "vegetables_required": ["egg", "onion", "tomato", "small_pepper"],
            "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Indian_Omelette.jpg/800px-Indian_Omelette.jpg",
            "time": "10 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Spicy Omelette recipe in Tamil")
        },
        {
            "name": "Thakkali Thokku (Tomato Relish)",
            "ingredients": ["5 Tomatoes", "Garlic", "Onion (optional)"],
            "steps": ["Heat sesame oil in a pan.", "Add smashed garlic cloves and highly chopped tomatoes.", "Cover and cook on low heat until it turns into a jam-like paste.", "Mix with plain rice or idli/dosa."],
            "vegetables_required": ["tomato", "garlic", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1588667500508-b1dc71be1d6d?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Thakkali Thokku recipe in Tamil")
        },
        {
            "name": "Vengaya Kosu (Onion Relish sides for Idli)",
            "ingredients": ["2 Onions", "1 Potato", "1 Tomato", "Garlic"],
            "steps": ["Boil and lightly mash the potato.", "Sauté onions and garlic until sweaty.", "Mix in the tomatoes and potato mash.", "Add slight tamarind water and simmer."],
            "vegetables_required": ["onion", "potato", "tomato", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Vengaya Kosu recipe in Tamil")
        },
        {
            "name": "Carrot Poriyal",
            "ingredients": ["3 Carrots", "1 Onion", "Grated Coconut"],
            "steps": ["Wash and grate the carrots.", "Temper mustard and curry leaves in hot oil.", "Sauté chopped onions, then add the grated carrots.", "Cover and cook for 5 mins, then garnish heavily with coconut."],
            "vegetables_required": ["carrot", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80",
            "time": "15 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Carrot Poriyal recipe in Tamil")
        },
        {
            "name": "Muttaikose Poriyal (Cabbage Fry)",
            "ingredients": ["Half Cabbage", "1 Onion", "Moong Dal (Optional)"],
            "steps": ["Finely shred the cabbage.", "Boil slightly with a pinch of turmeric.", "In a pan, sauté onions and mix the boiled cabbage.", "Top off with freshly grated coconut."],
            "vegetables_required": ["cabbage", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1614398751058-eb2e0bf63e53?auto=format&fit=crop&w=800&q=80",
            "time": "15 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Muttaikose Poriyal Cabbage recipe in Tamil")
        },
        {
            "name": "Cabbage Carrot Kootu",
            "ingredients": ["Cabbage", "Carrot", "Garlic", "Onion"],
            "steps": ["Chop the cabbage and carrots into small squares.", "Pressure cook them along with toor dal and chopped garlic.", "Temper mustard seeds and onions in a separate pan.", "Mix and boil together for 2 minutes."],
            "vegetables_required": ["cabbage", "carrot", "garlic", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Cabbage Carrot Kootu recipe in Tamil")
        },
        {
            "name": "Indo-Chinese Chilli Chicken (TN Style)",
            "ingredients": ["300g Chicken", "Bell Pepper", "Onion", "Garlic"],
            "steps": ["Fry small coated chicken cubes until fully cooked.", "In a hot wok, throw in cubic cut bell peppers, onions, and minced garlic.", "Sauté fast and mix the chicken pieces back in.", "Toss with soy sauce and serve hot."],
            "vegetables_required": ["chicken", "bell_pepper", "onion", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=800&q=80",
            "time": "35 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Chilli Chicken recipe in Tamil fast food style")
        },
        {
            "name": "Poondu Kuzhambu (Garlic Curry)",
            "ingredients": ["2 whole Garlics", "Onion", "Tomato", "Tamarind extract"],
            "steps": ["Peel tons of garlic cloves.", "Sauté small onions and garlic extensively in gingelly oil.", "Add tomato paste and let it melt.", "Pour tamarind water and boil till the oil floats to the top."],
            "vegetables_required": ["garlic", "onion", "tomato"],
            "imageUrl": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Poondu Kuzhambu Garlic Curry recipe in Tamil")
        },
        {
            "name": "Inji Kuzhambu (Ginger Digestion Curry)",
            "ingredients": ["Heavy portion of Ginger", "Garlic", "Onion", "Tomato"],
            "steps": ["Clean and chop ginger finely.", "Temper the pan and fry the ginger along with garlic and onions.", "Add tomatoes and tamarind.", "This acts as a medicinal curry to aid heavy stomach days."],
            "vegetables_required": ["ginger", "garlic", "onion", "tomato"],
            "imageUrl": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Inji Kuzhambu recipe in Tamil")
        },
        {
            "name": "Vellarikkai Thayir Pachadi (Cucumber Raita)",
            "ingredients": ["1 Cucumber", "Carrot", "Onion"],
            "steps": ["Grate the cucumber, drain excess water.", "Grate the carrot and chop some onions.", "Mix vegetables into a bowl of thick fresh curd/yogurt.", "Add salt and temper with roasted mustard and curry leaves."],
            "vegetables_required": ["cucumber", "carrot", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1555126634-ae231a47df6f?auto=format&fit=crop&w=800&q=80",
            "time": "10 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Vellarikkai Thayir Pachadi Cucumber Raita recipe in Tamil")
        },
        {
            "name": "Koyambedu Chilli Beef",
            "ingredients": ["500g Beef", "Bell Pepper", "Onion", "Garlic"],
            "steps": ["Prepare fried beef bits exactly like Chukka.", "Heat up a wok, adding squares of Bell Pepper and Onions.", "Toss it heavily with minced garlic.", "Serve directly from the wok."],
            "vegetables_required": ["beef", "bell_pepper", "onion", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1574484284002-952d92456975?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Chilli Beef recipe in Tamil street food")
        },
        {
            "name": "Kumquat Lemon Pickle (Oorugai TN style)",
            "ingredients": ["10 Kumquats", "Lemon Juice", "Garlic"],
            "steps": ["Slice the kumquats and remove seeds.", "Dry roast fenugreek and mustard seeds, powder them.", "Mix kumquats with salt and coat with the powder, along with a dash of lemon juice and garlic.", "Temper in oil and bottle it."],
            "vegetables_required": ["kumquat", "lemon", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1588667500508-b1dc71be1d6d?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Kumquat Pickle recipe in Tamil")
        },
        {
            "name": "Chicken Biryani (Dindigul Style)",
            "ingredients": ["500g Chicken", "Seeraga Samba Rice", "Onion", "Tomato", "Ginger", "Garlic", "Lemon"],
            "steps": ["Heat ghee in a pressure cooker.", "Make a green paste and ginger garlic paste. Sauté deeply with onions and tomatoes.", "Add the chicken, curd, and mint leaves.", "Add washed rice, squeeze half a lemon, and cook for 2 whistles."],
            "vegetables_required": ["chicken", "onion", "tomato", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1633383718081-22ac643dcd75?auto=format&fit=crop&w=800&q=80",
            "time": "60 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Dindigul Seeraga Samba Chicken Biryani recipe in Tamil")
        },
        {
            "name": "Shrimp Dum Biryani",
            "ingredients": ["400g Shrimp", "Basmati Rice", "Onion", "Tomato", "Garlic", "Ginger", "Lemon"],
            "steps": ["Marinate shrimp with lemon and spices.", "Prepare the gravy base using fried onions, ginger-garlic, and tomatoes.", "Drop the shrimp inside (only takes 5 minutes to cook).", "Layer with par-boiled rice and Dum for 15 mins on low heat."],
            "vegetables_required": ["shrimp", "onion", "tomato", "garlic", "ginger", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80",
            "time": "50 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Eral Dum Biryani Prawn recipe in Tamil")
        },
        {
            "name": "Egg Dum Biryani",
            "ingredients": ["4 Eggs", "Onion", "Tomato", "Ginger", "Garlic", "Lemon"],
            "steps": ["Boil and fry the eggs.", "Create biryani masala gravy with tomatoes, onions, ginger, and garlic.", "Pour in rice and water, squeezing the lemon.", "When water evaporates, push eggs underneath the rice and Dum."],
            "vegetables_required": ["egg", "onion", "tomato", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1589302168068-964664d93cb0?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Muttai Biryani Egg recipe in Tamil")
        },
        {
            "name": "Nattu Kozhi Rasam (Country Chicken Soup)",
            "ingredients": ["300g Chicken (bone-in)", "Small Pepper", "Garlic", "Tomato"],
            "steps": ["Crush garlic and small pepper heavily in a mortar.", "Boil the chicken with turmeric.", "Mix the pepper garlic mash and tomato into the boiling broth.", "A legendary cold and cough reliever in South India."],
            "vegetables_required": ["chicken", "small_pepper", "garlic", "tomato"],
            "imageUrl": "https://images.unsplash.com/photo-1563379926898-05f4575a4476?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Nattu Kozhi Rasam recipe in Tamil")
        },
        {
            "name": "Meen Puttu (Scrambled Fish)",
            "ingredients": ["300g Fish (Shark or Kingfish)", "Onion", "Garlic", "Ginger"],
            "steps": ["Boil the fish chunks.", "De-bone entirely and shred the meat.", "Temper a pan and sauté beautifully chopped onions, ginger, and garlic.", "Toss the shredded fish and scramble lightly. Do not add water."],
            "vegetables_required": ["fish", "onion", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1580476262798-b9030affcd58?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Sura Puttu Meen recipe in Tamil")
        },
        {
            "name": "Tofu Chettinad Masala (Veg Fusion)",
            "ingredients": ["200g Tofu", "Tomato", "Onion", "Garlic", "Ginger"],
            "steps": ["Cube and pan fry the Tofu softly.", "Dry roast Chettinad spices (fennel, cumin, pepper).", "Sauté onions, ginger, garlic, and tomato. Grind the roasted spices.", "Simmer everything together until Tofu absorbs the flavor."],
            "vegetables_required": ["tofu", "tomato", "onion", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Paneer Chettinad Masala recipe in Tamil")
        },
        {
            "name": "Eral Varuval (Spicy Prawn Dry Fry)",
            "ingredients": ["300g Shrimp", "Onion", "Tomato", "Garlic", "Ginger", "Lemon"],
            "steps": ["Sauté onions heavily into a pasty form.", "Add ginger garlic paste and finely chopped tomatoes.", "Toss shrimp inside, letting it release its own water.", "Dry roast on high heat, squeeze a hint of lemon, and serve crisp."],
            "vegetables_required": ["shrimp", "onion", "tomato", "garlic", "ginger", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1565557612660-84a1e0b57e75?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Eral Varuval Spicy Prawn Tamil")
        },
        {
            "name": "Thakkali Sadam (Tomato Rice)",
            "ingredients": ["Rice", "4 Tomatoes", "Onion", "Garlic"],
            "steps": ["Grind half the tomatoes into a puree, dice the rest.", "Sauté onions and garlic in a pressure cooker until brown.", "Add tomatoes, puree, salt, and biryani spices.", "Mix par-boiled rice, simmer for 1 whistle until flavored deeply."],
            "vegetables_required": ["tomato", "onion", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Thakkali Sadam Tomato Rice recipe in Tamil")
        },
        {
            "name": "Chicken Salna (Madurai Style)",
            "ingredients": ["1/2 kg Chicken", "Onion", "Tomato", "Ginger", "Garlic"],
            "steps": ["Grind roasted coconut, fennel, and onion into a paste.", "Sauté chopped onions and tomatoes with ginger-garlic paste.", "Add chicken and spices, then pour in the ground paste.", "Boil until the oil separates and the gravy thins out. Serve with Parotta."],
            "vegetables_required": ["chicken", "onion", "tomato", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Madurai Chicken Salna recipe in Tamil")
        },
        {
            "name": "Kanyakumari Fish Curry (Thengai Paal Meen Kuzhambu)",
            "ingredients": ["500g Fish", "Onion", "Tomato", "Ginger", "Garlic", "Lemon"],
            "steps": ["Extract thick coconut milk.", "Sauté onions, tomatoes, and ginger-garlic paste in coconut oil.", "Add water and spices, boil well.", "Add fish, simmer for 5 mins, then turn off heat and add coconut milk and a dash of lemon."],
            "vegetables_required": ["fish", "onion", "tomato", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1610729739502-3fe43ab03cb2?auto=format&fit=crop&w=800&q=80",
            "time": "35 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Kanyakumari Fish Curry recipe in Tamil")
        },
        {
            "name": "Pallipalayam Chicken Sukka",
            "ingredients": ["500g Chicken", "Small Pepper", "Onion", "Garlic"],
            "steps": ["Dry roast plenty of small green peppers and pound them.", "Fry tiny chopped onions and minced garlic in sesame oil.", "Add chicken and cook in its own juices.", "Sauté until crisp without adding any water."],
            "vegetables_required": ["chicken", "onion", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1626779430155-27aeb9e1fb56?auto=format&fit=crop&w=800&q=80",
            "time": "35 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Chicken Sukka recipe in Tamil")
        },
        {
            "name": "Eral 65 (Prawn 65)",
            "ingredients": ["250g Shrimp", "Ginger", "Garlic", "Lemon"],
            "steps": ["Clean and devein shrimp.", "Marinate with ginger-garlic paste, chili powder, salt, and lemon juice.", "Add a little cornflour to bind, then rest for 15 mins.", "Deep fry in hot oil until red and crispy."],
            "vegetables_required": ["shrimp", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1625943555419-56a2cb596640?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Prawn 65 Eral recipe in Tamil")
        },
        {
            "name": "Nanjil Nattu Beef Ularthiyathu",
            "ingredients": ["500g Beef", "Onion", "Ginger", "Garlic", "Small Pepper"],
            "steps": ["Cook beef with turmeric and salt in a pressure cooker.", "Crush ginger, garlic, and small green peppers together.", "Sauté heavily alongside diced onions in a cast iron pan.", "Dry roast the beef until intensely dark and coated with spices."],
            "vegetables_required": ["beef", "onion", "ginger", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1603048297172-c92544798d5e?auto=format&fit=crop&w=800&q=80",
            "time": "50 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Nanjil Nattu Beef recipe in Tamil")
        },
        {
            "name": "Roadside Kaalan (Mushroom/Cabbage Street Food)",
            "ingredients": ["Cabbage", "Onion", "Tomato", "Garlic", "Ginger"],
            "steps": ["Finely chop cabbage and fry into crispy pakoras.", "Prepare a thin gravy using onions, tomatoes, and ginger-garlic paste.", "Break the cabbage pakoras and mix into the boiling gravy.", "Serve hot garnished with raw onions."],
            "vegetables_required": ["cabbage", "onion", "tomato", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Roadside Kaalan Cabbage recipe in Tamil")
        },
        {
            "name": "Egg Kalaki (Street Style)",
            "ingredients": ["2 Eggs", "Onion", "Small Pepper", "Chicken Salna (Optional)"],
            "steps": ["Beat eggs in a glass.", "Add chopped onions, crushed small peppers, salt, and a splash of leftover chicken/meat gravy.", "Pour onto a tawa, fold instantly within 10 seconds while still semi-liquid inside.", "Serve immediately."],
            "vegetables_required": ["egg", "onion", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1510693206972-df098062cb71?auto=format&fit=crop&w=800&q=80",
            "time": "5 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Egg Kalaki street food recipe in Tamil")
        },
        {
            "name": "Pork Pepper Masala",
            "ingredients": ["500g Pork", "Onion", "Ginger", "Garlic", "Tomato"],
            "steps": ["Pressure cook pork with turmeric.", "Fry onions, tomatoes, and ginger-garlic paste until mushy.", "Add a generous amount of crushed black pepper and the cooked pork.", "Simmer until the gravy coats the meat deeply."],
            "vegetables_required": ["pork", "onion", "tomato", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1624933391986-778848db421a?auto=format&fit=crop&w=800&q=80",
            "time": "55 min",
            "difficulty": "Hard",
            "youtube_link": create_yt_link("Pork Pepper Masala recipe in Tamil")
        },
        {
            "name": "Muttai Kurma (Egg Coconut Curry)",
            "ingredients": ["4 Eggs", "Onion", "Tomato", "Ginger", "Garlic"],
            "steps": ["Boil and shell the eggs.", "Sauté onions, tomatoes, and ginger-garlic paste.", "Grind coconut with poppy seeds and add it to the onion-tomato base.", "Drop the eggs in and simmer for 10 minutes. Pairs well with Appam or Idiyappam."],
            "vegetables_required": ["egg", "onion", "tomato", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Muttai Kurma Egg Curry recipe in Tamil")
        },
        {
            "name": "Kudamilagai Muttai Poriyal (Capsicum Egg Scramble)",
            "ingredients": ["2 Eggs", "Bell Pepper", "Onion"],
            "steps": ["Chop onions and bell pepper (capsicum) finely.", "Sauté in a pan until slightly soft but still crunchy.", "Crack eggs into the pan, season with salt and pepper.", "Scramble evenly and serve hot."],
            "vegetables_required": ["egg", "bell_pepper", "onion"],
            "imageUrl": "https://images.unsplash.com/photo-1614398751058-eb2e0bf63e53?auto=format&fit=crop&w=800&q=80",
            "time": "15 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Capsicum Egg Muttai Poriyal recipe in Tamil")
        },
        {
            "name": "Fish Milagu Thokku (Pepper Fish Relish)",
            "ingredients": ["300g Fish (Boneless)", "Onion", "Tomato", "Garlic", "Ginger"],
            "steps": ["Sauté onions, ginger, and garlic intensely in gingelly oil.", "Add tomatoes and mash them down.", "Place boneless fish pieces inside along with a heavy dose of crushed black pepper.", "Cover and cook slowly until it becomes a rich, thick relish."],
            "vegetables_required": ["fish", "onion", "tomato", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1599084924616-e9b0183354f9?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Fish Pepper Thokku recipe in Tamil")
        },
        {
            "name": "Tomato Garlic Rasam",
            "ingredients": ["3 Tomatoes", "Garlic", "Small Pepper", "Lemon"],
            "steps": ["Mash tomatoes by hand in water along with tamarind extract.", "Coarsely crush garlic and small peppers in a mortar.", "Temper mustard and cumin, add the crushed mix, then pour the tomato water.", "Let it froth (do not boil excessively). Squeeze lemon off-heat."],
            "vegetables_required": ["tomato", "garlic", "small_pepper", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80",
            "time": "15 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Thakkali Poondu Rasam recipe in Tamil")
        },
        {
            "name": "Carrot Cucumber Kosambari (Salad)",
            "ingredients": ["Carrot", "Cucumber", "Lemon"],
            "steps": ["Grate the carrot and chop the cucumber very finely.", "Mix together in a bowl with a pinch of salt.", "Squeeze fresh lemon juice over the top.", "Temper with mustard seeds and mix well (yogurt optional)."],
            "vegetables_required": ["carrot", "cucumber", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
            "time": "10 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Carrot Kosambari recipe in Tamil")
        },
        {
            "name": "Cauliflower Milagu Varuval",
            "ingredients": ["1 Cauliflower", "Onion", "Garlic", "Small Pepper"],
            "steps": ["Blanch cauliflower in boiling salted water.", "Heat oil, sauté onions, crushed garlic, and small green peppers.", "Toss the cauliflower in and stir fry on high heat.", "Finish with freshly ground black pepper for extra kick."],
            "vegetables_required": ["cauliflower", "onion", "garlic", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1555126634-ae231a47df6f?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Cauliflower Pepper Fry recipe in Tamil")
        },
        {
            "name": "Tofu 65 (Vegetarian Starter)",
            "ingredients": ["200g Tofu", "Ginger", "Garlic", "Lemon"],
            "steps": ["Press the tofu to remove water, then cut into tight cubes.", "Make a thick paste with ginger-garlic, chili powder, rice flour, and lemon juice.", "Coat the tofu cubes evenly.", "Shallow fry or air fry until a crispy outer shell forms."],
            "vegetables_required": ["tofu", "ginger", "garlic", "lemon"],
            "imageUrl": "https://images.unsplash.com/photo-1588667500508-b1dc71be1d6d?auto=format&fit=crop&w=800&q=80",
            "time": "20 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Paneer 65 Tofu recipe in Tamil")
        },
        {
            "name": "Shrimp Cauliflower Stir Fry (Eral Gobi Varuval)",
            "ingredients": ["200g Shrimp", "Cauliflower", "Onion", "Tomato", "Ginger", "Garlic"],
            "steps": ["Clean shrimp and blanch cauliflower florets.", "Sauté onions, tomatoes, and ginger-garlic into a thick base.", "Toss in both shrimp and cauliflower.", "Stir fry for 6-8 minutes until shrimp curls and cooks."],
            "vegetables_required": ["shrimp", "cauliflower", "onion", "tomato", "ginger", "garlic"],
            "imageUrl": "https://images.unsplash.com/photo-1559742811-822873691fc8?auto=format&fit=crop&w=800&q=80",
            "time": "25 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Eral Cauliflower Poriyal recipe in Tamil")
        },
        {
            "name": "Kumbakonam Chicken Curry",
            "ingredients": ["500g Chicken", "Onion", "Tomato", "Garlic", "Ginger"],
            "steps": ["Dry roast coriander, cumin, and dry chilies, then powder.", "Sauté onions, tomatoes, ginger, and garlic intensely.", "Add the spice powder and the chicken.", "Slow cook with a little water until thick and aromatic."],
            "vegetables_required": ["chicken", "onion", "tomato", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=800&q=80",
            "time": "45 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Kumbakonam Chicken Curry recipe in Tamil")
        },
        {
            "name": "Spicy Tomato Potato Kurma (Aloo Tomato Mash)",
            "ingredients": ["3 Potatoes", "3 Tomatoes", "Onion", "Garlic", "Ginger"],
            "steps": ["Boil and mash the potatoes.", "Heat oil, fry ginger-garlic, onions, and lots of tomatoes into a paste.", "Mix the mashed potatoes and add a touch of water.", "Cook until the gravy thickens perfectly for Pooris or Chapathi."],
            "vegetables_required": ["potato", "tomato", "onion", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
            "time": "30 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Poori Kizhangu Masala recipe in Tamil")
        },
        {
            "name": "Cabbage Muttai Poriyal (Cabbage Egg Fry)",
            "ingredients": ["Cabbage", "2 Eggs", "Onion", "Small Pepper"],
            "steps": ["Chop the cabbage and onions extremely finely.", "Sauté them with small green peppers until the cabbage shrinks and cooks.", "Push vegetables to the side of the pan and crack the eggs.", "Scramble the eggs, then mix everything together."],
            "vegetables_required": ["cabbage", "egg", "onion", "small_pepper"],
            "imageUrl": "https://images.unsplash.com/photo-1614398751058-eb2e0bf63e53?auto=format&fit=crop&w=800&q=80",
            "time": "15 min",
            "difficulty": "Easy",
            "youtube_link": create_yt_link("Muttaikose Muttai Poriyal recipe in Tamil")
        },
        {
            "name": "Beef Keema Masala (Kothu Kari)",
            "ingredients": ["300g Minced Beef", "Onion", "Tomato", "Garlic", "Ginger"],
            "steps": ["Wash the minced beef carefully.", "Sauté finely chopped onions, tomatoes, and ginger-garlic paste into a thick masala.", "Add the minced meat and stir continuously to prevent lumps.", "Cook on low heat until the meat is fully roasted and oil is released."],
            "vegetables_required": ["beef", "onion", "tomato", "garlic", "ginger"],
            "imageUrl": "https://images.unsplash.com/photo-1544025162-811cba1714fc?auto=format&fit=crop&w=800&q=80",
            "time": "40 min",
            "difficulty": "Medium",
            "youtube_link": create_yt_link("Beef Kothukari Madurai style recipe in Tamil")
        }
    ]

    # 4. Insert into database
    recipes_collection.insert_many(real_recipes)
    print(f"[OK] Successfully inserted {len(real_recipes)} Authentic Tamil recipes with Search Links into MongoDB!")

except Exception as e:
    print(f"[ERROR] Error connecting to MongoDB: {e}")
