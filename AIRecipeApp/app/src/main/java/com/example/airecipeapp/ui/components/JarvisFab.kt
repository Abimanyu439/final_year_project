package com.example.airecipeapp.ui.components

import android.app.Activity
import android.content.Intent
import android.speech.RecognizerIntent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.*
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.airecipeapp.ui.viewmodel.JarvisState
import com.example.airecipeapp.ui.viewmodel.JarvisViewModel
import java.util.Locale

@Composable
fun JarvisFab(
    jarvisViewModel: JarvisViewModel = viewModel()
) {
    val state = jarvisViewModel.state

    val speechLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data = result.data
            val matches = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if (!matches.isNullOrEmpty()) {
                val spokenText = matches[0]
                jarvisViewModel.processSpokenText(spokenText)
            } else {
                jarvisViewModel.resetState()
            }
        } else {
            jarvisViewModel.resetState()
        }
    }

    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val scale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = if (state is JarvisState.Thinking || state is JarvisState.Speaking) 1.15f else 1f,
        animationSpec = infiniteRepeatable(animation = tween(600, easing = LinearEasing), repeatMode = RepeatMode.Reverse),
        label = "scale"
    )

    val fabColor by animateColorAsState(
        targetValue = when (state) {
            is JarvisState.Idle -> MaterialTheme.colorScheme.primary
            is JarvisState.Listening -> Color.Red
            is JarvisState.Thinking -> Color(0xFFFF9800) // Orange
            is JarvisState.Speaking -> Color(0xFF4CAF50) // Green
            is JarvisState.Error -> Color.DarkGray
        }, label = "color"
    )

    FloatingActionButton(
        onClick = {
            if (state is JarvisState.Idle || state is JarvisState.Error || state is JarvisState.Speaking) {
                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
                    putExtra(RecognizerIntent.EXTRA_PROMPT, "Hello! Ask me about recipes...")
                }
                try {
                    speechLauncher.launch(intent)
                } catch (e: Exception) {
                    // Ignore if device doesn't support speech
                }
            }
        },
        containerColor = fabColor,
        contentColor = Color.White,
        modifier = Modifier.scale(scale).size(64.dp)
    ) {
        Icon(Icons.Default.Mic, contentDescription = "Ask Jarvis", modifier = Modifier.size(28.dp))
    }
}