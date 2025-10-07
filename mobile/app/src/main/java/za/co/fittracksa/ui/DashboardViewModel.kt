package za.co.fittracksa.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import za.co.fittracksa.domain.ActivityRepository
import za.co.fittracksa.domain.NutritionRepository
import za.co.fittracksa.domain.SettingsRepository
import za.co.fittracksa.data.api.SettingsUpdate
import za.co.fittracksa.data.local.PendingActivityEntity
import za.co.fittracksa.data.local.PendingMealEntity
import javax.inject.Inject

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val activityRepository: ActivityRepository,
    private val nutritionRepository: NutritionRepository,
    private val settingsRepository: SettingsRepository,
) : ViewModel() {

    private val _state = MutableStateFlow(DashboardState(0, 0, true, "", 0))
    val state: StateFlow<DashboardState> = _state

    fun queueActivity(activity: PendingActivityEntity) {
        viewModelScope.launch {
            activityRepository.queueActivity(activity)
        }
    }

    fun queueMeal(meal: PendingMealEntity) {
        viewModelScope.launch {
            nutritionRepository.queueMeal(meal)
        }
    }

    fun updateSettings(token: String, language: String, notifications: Boolean, hydration: Boolean) {
        viewModelScope.launch {
            val response = settingsRepository.update(
                token,
                SettingsUpdate(language = language, notificationsEnabled = notifications, hydrationReminders = hydration),
            )
            _state.value = _state.value.copy(
                hydrationReminder = response.hydrationReminders,
            )
        }
    }
}
