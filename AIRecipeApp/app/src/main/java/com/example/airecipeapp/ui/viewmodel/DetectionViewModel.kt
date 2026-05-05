package com.example.airecipeapp.ui.viewmodel

import androidx.compose.runtime.mutableStateListOf
import androidx.lifecycle.ViewModel
import com.example.airecipeapp.network.Recipe

class DetectionViewModel : ViewModel() {
    var detectedVegetables = mutableStateListOf<String>()

    // 🚨 SPLIT INTO TWO LISTS 🚨
    var exactMatches = mutableStateListOf<Recipe>()
    var furtherRecommendations = mutableStateListOf<Recipe>()

    fun updateResults(vegs: List<String>, exact: List<Recipe>, further: List<Recipe>) {
        detectedVegetables.clear()
        detectedVegetables.addAll(vegs)

        exactMatches.clear()
        exactMatches.addAll(exact)

        furtherRecommendations.clear()
        furtherRecommendations.addAll(further)
    }
}