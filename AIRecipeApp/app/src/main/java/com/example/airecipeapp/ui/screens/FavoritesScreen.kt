package com.example.airecipeapp.ui.screens

import com.example.airecipeapp.data.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.airecipeapp.data.FavoriteManager
import com.example.airecipeapp.navigation.Screen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FavoritesScreen(navController: NavController) {
    val favorites = FavoriteManager.favoriteRecipes

    Scaffold(
        topBar = { TopAppBar(title = { Text("Saved Recipes") }) }
    ) { padding ->
        if (favorites.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("No saved recipes yet!", color = androidx.compose.ui.graphics.Color.Gray)
            }
        } else {
            LazyColumn(contentPadding = padding) {
                items(favorites) { recipe ->
                    RecipeCard(recipe) {
                        navController.navigate(Screen.RecipeDetail.createRoute(recipe.name))
                    }
                }
            }
        }
    }
}