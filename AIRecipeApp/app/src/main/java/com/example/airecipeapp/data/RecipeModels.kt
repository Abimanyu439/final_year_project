package com.example.airecipeapp.data

import androidx.compose.runtime.mutableStateListOf
import com.example.airecipeapp.network.Recipe

object FavoriteManager {
    val favoriteRecipes = mutableStateListOf<Recipe>()

    fun toggleFavorite(recipe: Recipe) {
        if (favoriteRecipes.any { it.name == recipe.name }) {
            favoriteRecipes.removeAll { it.name == recipe.name }
        } else {
            favoriteRecipes.add(recipe)
        }
    }

    fun isFavorite(recipeName: String): Boolean {
        return favoriteRecipes.any { it.name == recipeName }
    }
}

object FeaturedData {
    val trendingRecipes = listOf(
        Recipe(
            name = "Chettinad Chicken Curry",
            ingredients = listOf("500g Chicken", "Onion", "Tomato", "Ginger", "Garlic", "Lemon"),
            steps = listOf("Marinate chicken with lemon.", "Sauté ginger-garlic and onions.", "Add tomatoes and spices.", "Cook until tender."),
            imageUrl = "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?q=80&w=1000",
            time = "45 min",
            difficulty = "Medium",
            youtube_link = "https://www.youtube.com/watch?v=zR2R652gGjU",
            match_score = 100.0
        ),
        Recipe(
            name = "Spicy Fish Fry",
            ingredients = listOf("Fish", "Lemon", "Ginger", "Garlic", "Chilli powder"),
            steps = listOf("Apply masala paste.", "Marinate 20 mins.", "Shallow fry until crispy."),
            imageUrl = "https://images.unsplash.com/photo-1599084924616-e9b0183354f9?q=80&w=1000",
            time = "25 min",
            difficulty = "Easy",
            youtube_link = "https://www.youtube.com/watch?v=0k5nB76j7Bw",
            match_score = 100.0
        )
    )
}