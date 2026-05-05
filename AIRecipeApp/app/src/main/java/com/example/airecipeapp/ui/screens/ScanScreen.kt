package com.example.airecipeapp.ui.screens

import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.example.airecipeapp.navigation.Screen
import com.example.airecipeapp.network.*
import com.example.airecipeapp.ui.viewmodel.DetectionViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

@Composable
fun ScanScreen(navController: NavController, viewModel: DetectionViewModel) {
    var isDetecting by remember { mutableStateOf(false) }
    val selectedImages = remember { mutableStateListOf<Uri>() }
    val context = LocalContext.current

    val photoPicker = rememberLauncherForActivityResult(ActivityResultContracts.PickMultipleVisualMedia()) { uris ->
        selectedImages.addAll(uris)
    }

    val cameraLauncher = rememberLauncherForActivityResult(ActivityResultContracts.TakePicturePreview()) { bitmap ->
        if (bitmap != null) {
            val file = File(context.cacheDir, "camera_${System.currentTimeMillis()}.jpg")
            file.outputStream().use {
                bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 100, it)
            }
            selectedImages.add(Uri.fromFile(file))
        }
    }

    LaunchedEffect(isDetecting) {
        if (isDetecting && selectedImages.isNotEmpty()) {
            try {
                val allVegs = mutableSetOf<String>()

                for (uri in selectedImages) {
                    val file = uriToFile(context, uri)
                    val requestFile = file.asRequestBody("image/jpeg".toMediaTypeOrNull())
                    val body = MultipartBody.Part.createFormData("image", file.name, requestFile)
                    val response = RetrofitClient.api.detectVegetables(body)
                    response.vegetables.forEach { allVegs.add(it) }
                }

                val vegList = allVegs.toList()
                var exactRecipes = emptyList<Recipe>()
                var furtherRecipes = emptyList<Recipe>()

                if (vegList.isNotEmpty()) {
                    val recResponse = RetrofitClient.api.getRecommendations(RecommendRequest(vegList))
                    // 🚨 SEPARATE THE RESPONSES SAFELY 🚨
                    exactRecipes = recResponse.exact_matches ?: emptyList()
                    furtherRecipes = recResponse.further_recommendations ?: emptyList()
                }

                withContext(Dispatchers.Main) {
                    viewModel.updateResults(vegList, exactRecipes, furtherRecipes)
                    isDetecting = false
                    navController.navigate(Screen.RecipeList.route)
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    isDetecting = false
                    viewModel.updateResults(emptyList(), emptyList(), emptyList())
                    Toast.makeText(context, "AI Analysis Error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    Column(Modifier.fillMaxSize().padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Text("Scan Ingredients", style = MaterialTheme.typography.headlineMedium)
        Text("Add up to 5 photos", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
        Spacer(Modifier.height(20.dp))
        Box(Modifier.fillMaxWidth().height(250.dp).background(Color(0xFFF5F5F5), RoundedCornerShape(16.dp)).border(1.dp, Color.Gray, RoundedCornerShape(16.dp)), contentAlignment = Alignment.Center) {
            if (selectedImages.isEmpty()) Icon(Icons.Default.Image, null, Modifier.size(48.dp), tint = Color.Gray)
            else LazyRow { items(selectedImages) { uri -> AsyncImage(uri, null, Modifier.size(200.dp).padding(8.dp).clip(RoundedCornerShape(12.dp)), contentScale = ContentScale.Crop) } }
        }
        Spacer(Modifier.height(20.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(
                onClick = { cameraLauncher.launch(null) },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFAEC4FF))
            ) {
                Text("+ Camera", color = Color.Black)
            }
            OutlinedButton(onClick = { photoPicker.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)) }) { 
                Text("Upload Gallery") 
            }
            if (selectedImages.isNotEmpty()) OutlinedButton(onClick = { selectedImages.clear() }) { Text("Clear") }
        }
        Spacer(Modifier.height(40.dp))
        Button(onClick = { isDetecting = true }, modifier = Modifier.fillMaxWidth().height(56.dp), enabled = !isDetecting && selectedImages.isNotEmpty()) {
            if (isDetecting) CircularProgressIndicator(Modifier.size(24.dp), color = Color.White) else Text("Analyze & Identify Vegetables")
        }
    }
}

fun uriToFile(context: android.content.Context, uri: Uri): File {
    val file = File(context.cacheDir, "temp_${System.currentTimeMillis()}.jpg")
    context.contentResolver.openInputStream(uri)?.use { input -> FileOutputStream(file).use { output -> input.copyTo(output) } }
    return file
}