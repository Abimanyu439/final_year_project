package com.example.airecipeapp.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.example.airecipeapp.navigation.Screen
import com.example.airecipeapp.ui.viewmodel.DetectionViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeListScreen(navController: NavController, viewModel: DetectionViewModel) {
    val detectedVegetables = viewModel.detectedVegetables
    val exactMatches = viewModel.exactMatches
    val furtherRecommendations = viewModel.furtherRecommendations

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("AI Analysis Results", fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = { navController.popBackStack() }) { Icon(Icons.Default.ArrowBack, "Back") } }
            )
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding).padding(horizontal = 16.dp)) {

            // 1. Ingredients Section
            item {
                Spacer(Modifier.height(16.dp))
                Text("AI Identified Ingredients", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.height(12.dp))

                if (detectedVegetables.isEmpty()) {
                    Surface(color = Color(0xFFFFEBEE), shape = RoundedCornerShape(12.dp), modifier = Modifier.fillMaxWidth()) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Info, null, tint = Color.Red)
                            Spacer(Modifier.width(12.dp))
                            Text("No vegetables detected.", color = Color(0xFFB71C1C))
                        }
                    }
                } else {
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        items(detectedVegetables) { veg ->
                            AssistChip(onClick = { }, label = { Text(veg.replaceFirstChar { it.uppercase() }) }, leadingIcon = { Icon(Icons.Default.Check, null, Modifier.size(18.dp)) })
                        }
                    }
                }
                Spacer(Modifier.height(24.dp))
            }

            // 2. Empty State
            if (detectedVegetables.isNotEmpty() && exactMatches.isEmpty() && furtherRecommendations.isEmpty()) {
                item { Text("No matching recipes found.", color = Color.Gray, modifier = Modifier.padding(vertical = 16.dp)) }
            }

            // 3. Exact Matches Section
            if (exactMatches.isNotEmpty()) {
                item {
                    Text("Exact Matches (Ready to Cook!)", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Color(0xFF2E7D32))
                    Spacer(Modifier.height(12.dp))
                }
                items(exactMatches) { recipe ->
                    RecipeCard(recipe = recipe) { navController.navigate(Screen.RecipeDetail.createRoute(recipe.name)) }
                }
                item { Spacer(Modifier.height(16.dp)) }
            }

            // 4. Further Recommendations Section
            if (furtherRecommendations.isNotEmpty()) {
                item {
                    Text("Other Suggestions (Need more ingredients)", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Color(0xFFF57C00))
                    Spacer(Modifier.height(12.dp))
                }
                items(furtherRecommendations) { recipe ->
                    RecipeCard(recipe = recipe) { navController.navigate(Screen.RecipeDetail.createRoute(recipe.name)) }
                }
            }

            item { Spacer(Modifier.height(50.dp)) }
        }
    }
}

@Composable
fun RecipeCard(recipe: com.example.airecipeapp.network.Recipe, onClick: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp).clickable { onClick() }, elevation = CardDefaults.cardElevation(4.dp), shape = RoundedCornerShape(16.dp)) {
        Column {
            Box {
                AsyncImage(model = recipe.imageUrl, contentDescription = null, modifier = Modifier.height(180.dp).fillMaxWidth(), contentScale = ContentScale.Crop)
                Surface(modifier = Modifier.padding(12.dp).align(Alignment.TopEnd), color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(8.dp)) {
                    Text("${recipe.match_score.toInt()}% Match", modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp), style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
                }
            }
            Column(modifier = Modifier.padding(16.dp)) {
                Text(recipe.name, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Timer, null, Modifier.size(16.dp), Color.Gray)
                        Spacer(Modifier.width(4.dp))
                        Text(recipe.time, color = Color.Gray, style = MaterialTheme.typography.bodySmall)
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Restaurant, null, Modifier.size(16.dp), Color.Gray)
                        Spacer(Modifier.width(4.dp))
                        Text(recipe.difficulty, color = Color.Gray, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}