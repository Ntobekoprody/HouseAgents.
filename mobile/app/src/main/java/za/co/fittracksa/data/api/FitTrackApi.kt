package za.co.fittracksa.data.api

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST

interface FitTrackApi {
    @POST("/register")
    suspend fun register(@Body payload: RegisterRequest): UserResponse

    @POST("/auth/login")
    suspend fun login(@Body payload: LoginRequest): TokenResponse

    @GET("/activities")
    suspend fun activities(@Header("Authorization") bearer: String): List<ActivityResponse>

    @POST("/activities")
    suspend fun createActivity(
        @Header("Authorization") bearer: String,
        @Body payload: ActivityRequest,
    ): ActivityResponse

    @GET("/nutrition")
    suspend fun nutrition(@Header("Authorization") bearer: String): List<NutritionResponse>

    @POST("/nutrition")
    suspend fun createNutrition(
        @Header("Authorization") bearer: String,
        @Body payload: NutritionRequest,
    ): NutritionResponse

    @GET("/settings")
    suspend fun settings(@Header("Authorization") bearer: String): SettingsResponse

    @PATCH("/settings")
    suspend fun updateSettings(
        @Header("Authorization") bearer: String,
        @Body payload: SettingsUpdate,
    ): SettingsResponse
}

@Serializable
data class RegisterRequest(val email: String, val password: String)

@Serializable
data class LoginRequest(val email: String, val password: String)

@Serializable
data class TokenResponse(@SerialName("access_token") val accessToken: String)

@Serializable
data class ActivityRequest(
    val type: String,
    @SerialName("duration_minutes") val durationMinutes: Int,
    @SerialName("calories_burned") val caloriesBurned: Int,
    val steps: Int? = null,
    @SerialName("perceived_effort") val perceivedEffort: String? = null,
    val notes: String? = null,
)

@Serializable
data class ActivityResponse(
    val id: Int,
    val type: String,
    @SerialName("duration_minutes") val durationMinutes: Int,
    @SerialName("calories_burned") val caloriesBurned: Int,
    val steps: Int? = null,
    val timestamp: String,
)

@Serializable
data class NutritionRequest(
    @SerialName("food_item") val foodItem: String,
    val calories: Int,
    @SerialName("meal_type") val mealType: String? = null,
)

@Serializable
data class NutritionResponse(
    val id: Int,
    @SerialName("food_item") val foodItem: String,
    val calories: Int,
    @SerialName("meal_type") val mealType: String? = null,
    val timestamp: String,
)

@Serializable
data class SettingsUpdate(
    val language: String? = null,
    @SerialName("notifications_enabled") val notificationsEnabled: Boolean? = null,
    @SerialName("hydration_reminders") val hydrationReminders: Boolean? = null,
)

@Serializable
data class SettingsResponse(
    val language: String,
    @SerialName("notifications_enabled") val notificationsEnabled: Boolean,
    @SerialName("hydration_reminders") val hydrationReminders: Boolean,
    val timezone: String? = null,
)

@Serializable
data class UserResponse(val id: Int, val email: String)
