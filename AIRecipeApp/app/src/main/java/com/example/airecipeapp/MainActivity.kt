package com.example.airecipeapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument

import com.example.airecipeapp.data.FeaturedData
import com.example.airecipeapp.navigation.Screen
import com.example.airecipeapp.ui.components.BottomNavBar
import com.example.airecipeapp.ui.screens.*
import com.example.airecipeapp.ui.theme.AIRecipeAppTheme
import com.example.airecipeapp.ui.viewmodel.DetectionViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AIRecipeAppTheme {
                MainApp()
            }
        }
    }
}

@Composable
fun MainApp() {
    val navController = rememberNavController()
    val detectionViewModel: DetectionViewModel = viewModel()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val showBottomBar = currentRoute in listOf(
        Screen.Home.route, Screen.Scan.route, Screen.Favorites.route, Screen.Profile.route
    )

    Scaffold(bottomBar = { if (showBottomBar) BottomNavBar(navController) }) { innerPadding ->
        NavHost(navController = navController, startDestination = Screen.Splash.route, modifier = Modifier.padding(innerPadding)) {
            composable(Screen.Splash.route) { SplashScreen(navController) }
            composable(Screen.Login.route) { LoginScreen(navController) }
            composable(Screen.Home.route) { HomeScreen(navController) }
            composable(Screen.Scan.route) { ScanScreen(navController, detectionViewModel) }
            composable(Screen.RecipeList.route) { RecipeListScreen(navController, detectionViewModel) }

            composable(
                route = Screen.RecipeDetail.route,
                arguments = listOf(navArgument("recipeName") { type = NavType.StringType })
            ) { backStackEntry ->
                val recipeName = backStackEntry.arguments?.getString("recipeName") ?: ""

                // 🚨 SEARCH THROUGH ALL 3 LISTS TO FIND THE CLICKED RECIPE 🚨
                val allRecipes = FeaturedData.trendingRecipes +
                        detectionViewModel.exactMatches +
                        detectionViewModel.furtherRecommendations

                val recipe = allRecipes.find { it.name == recipeName }

                if (recipe != null) {
                    RecipeDetailScreen(navController, recipe)
                } else {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("Recipe details not found.", color = MaterialTheme.colorScheme.error)
                    }
                }
            }

            composable(Screen.Favorites.route) { FavoritesScreen(navController) }
            composable(Screen.Profile.route) { ProfileScreen() }
        }
    }
}