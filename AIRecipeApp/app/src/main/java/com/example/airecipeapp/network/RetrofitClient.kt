package com.example.airecipeapp.network

import com.google.gson.annotations.SerializedName
import okhttp3.*
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

data class DetectResponse(@SerializedName("vegetables") val vegetables: List<String>)
data class RecommendRequest(@SerializedName("vegetables") val vegetables: List<String>)
data class JarvisRequest(@SerializedName("text") val text: String)

data class Recipe(
    @SerializedName("name") val name: String,
    @SerializedName("ingredients") val ingredients: List<String>,
    @SerializedName("steps") val steps: List<String>,
    @SerializedName("imageUrl") val imageUrl: String,
    @SerializedName("time") val time: String,
    @SerializedName("difficulty") val difficulty: String,
    @SerializedName("youtube_link") val youtube_link: String,
    @SerializedName("match_score") val match_score: Double
)

data class RecommendResponse(
    @SerializedName("identified_ingredients") val identified_ingredients: List<String>? = null,
    @SerializedName("exact_matches") val exact_matches: List<Recipe>? = null,
    @SerializedName("further_recommendations") val further_recommendations: List<Recipe>? = null
)

data class JarvisResponse(@SerializedName("response") val response: String)

interface ApiService {
    @Multipart
    @POST("detect")
    suspend fun detectVegetables(@Part image: MultipartBody.Part): DetectResponse

    @POST("recommend")
    suspend fun getRecommendations(@Body request: RecommendRequest): RecommendResponse

    @POST("jarvis")
    suspend fun askJarvis(@Body request: JarvisRequest): JarvisResponse
}

object RetrofitClient {
    // 🚨 UPDATE THIS URL TO MATCH YOUR CURRENT NGROK URL 🚨
    private const val BASE_URL = "https://hatbox-shindig-counting.ngrok-free.dev"

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(60, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    val api: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}