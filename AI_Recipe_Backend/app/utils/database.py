from pymongo import MongoClient

# Use local MongoDB or MongoDB Atlas URI
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

db = client.ai_recipe_db
recipes_collection = db.recipes