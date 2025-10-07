package za.co.fittracksa.domain

import kotlinx.coroutines.flow.first
import za.co.fittracksa.data.api.ActivityRequest
import za.co.fittracksa.data.api.FitTrackApi
import za.co.fittracksa.data.api.LoginRequest
import za.co.fittracksa.data.api.NutritionRequest
import za.co.fittracksa.data.api.RegisterRequest
import za.co.fittracksa.data.api.SettingsResponse
import za.co.fittracksa.data.api.SettingsUpdate
import za.co.fittracksa.data.local.OfflineQueueDao
import za.co.fittracksa.data.local.PendingActivityEntity
import za.co.fittracksa.data.local.PendingMealEntity

class AuthRepository(private val api: FitTrackApi) {
    suspend fun register(email: String, password: String) = api.register(RegisterRequest(email, password))
    suspend fun login(email: String, password: String) = api.login(LoginRequest(email, password))
}

class ActivityRepository(
    private val api: FitTrackApi,
    private val dao: OfflineQueueDao,
) {
    suspend fun syncPending(token: String) {
        val bearer = "Bearer $token"
        dao.pendingActivities().first().forEach { pending ->
            api.createActivity(
                bearer,
                ActivityRequest(
                    type = pending.type,
                    durationMinutes = pending.durationMinutes,
                    caloriesBurned = pending.caloriesBurned,
                    steps = pending.steps,
                    perceivedEffort = pending.perceivedEffort,
                    notes = pending.notes,
                ),
            )
            dao.deleteActivity(pending.id)
        }
    }

    suspend fun queueActivity(entity: PendingActivityEntity) = dao.insertActivity(entity)
}

class NutritionRepository(
    private val api: FitTrackApi,
    private val dao: OfflineQueueDao,
) {
    suspend fun syncPending(token: String) {
        val bearer = "Bearer $token"
        dao.pendingMeals().first().forEach { pending ->
            api.createNutrition(
                bearer,
                NutritionRequest(
                    foodItem = pending.foodItem,
                    calories = pending.calories,
                    mealType = pending.mealType,
                ),
            )
            dao.deleteMeal(pending.id)
        }
    }

    suspend fun queueMeal(entity: PendingMealEntity) = dao.insertMeal(entity)
}

class SettingsRepository(private val api: FitTrackApi) {
    suspend fun load(token: String): SettingsResponse = api.settings("Bearer $token")
    suspend fun update(token: String, update: SettingsUpdate): SettingsResponse =
        api.updateSettings("Bearer $token", update)
}
