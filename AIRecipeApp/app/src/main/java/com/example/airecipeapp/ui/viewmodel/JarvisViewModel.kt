package com.example.airecipeapp.ui.viewmodel

import android.app.Application
import android.speech.tts.TextToSpeech
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.airecipeapp.network.JarvisRequest
import com.example.airecipeapp.network.RetrofitClient
import kotlinx.coroutines.launch
import java.util.Locale

sealed class JarvisState {
    object Idle : JarvisState()
    object Listening : JarvisState()
    object Thinking : JarvisState()
    data class Speaking(val response: String) : JarvisState()
    data class Error(val message: String) : JarvisState()
}

class JarvisViewModel(application: Application) : AndroidViewModel(application) {

    var state by mutableStateOf<JarvisState>(JarvisState.Idle)
        private set

    var lastUserText by mutableStateOf("")
        private set

    private var textToSpeech: TextToSpeech? = null

    init {
        // Setup Android Text-To-Speech
        textToSpeech = TextToSpeech(application) { status ->
            if (status == TextToSpeech.SUCCESS) {
                textToSpeech?.language = Locale.US
            }
        }
    }

    fun processSpokenText(spokenText: String) {
        lastUserText = spokenText
        state = JarvisState.Thinking

        viewModelScope.launch {
            try {
                // Call Python FastAPI
                val apiResponse = RetrofitClient.api.askJarvis(JarvisRequest(spokenText))
                val aiReply = apiResponse.response

                state = JarvisState.Speaking(aiReply)

                // Speak out loud!
                textToSpeech?.speak(aiReply, TextToSpeech.QUEUE_FLUSH, null, null)

            } catch (e: Exception) {
                state = JarvisState.Error(e.message ?: "Network error")
                textToSpeech?.speak("Sorry, I could not connect to the server.", TextToSpeech.QUEUE_FLUSH, null, null)
            }
        }
    }

    fun resetState() {
        state = JarvisState.Idle
    }

    override fun onCleared() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        super.onCleared()
    }
}