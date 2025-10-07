package za.co.fittracksa.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "pending_activity")
data class PendingActivityEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val type: String,
    val durationMinutes: Int,
    val caloriesBurned: Int,
    val steps: Int?,
    val perceivedEffort: String?,
    val notes: String?,
)

@Entity(tableName = "pending_meal")
data class PendingMealEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val foodItem: String,
    val calories: Int,
    val mealType: String?,
)
