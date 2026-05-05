package com.example.airecipeapp.navigation

sealed class Screen(val route: String) {
    object Splash : Screen("splash")
    object Login : Screen("login")
    object Home : Screen("home")
    object Scan : Screen("scan")
    object RecipeList : Screen("recipe_list") // Result after scan
    object RecipeDetail : Screen("recipe_detail/{recipeName}") {
        fun createRoute(recipeName: String) = "recipe_detail/$recipeName"
    }
    object Favorites : Screen("favorites")
    object Profile : Screen("profile")
}