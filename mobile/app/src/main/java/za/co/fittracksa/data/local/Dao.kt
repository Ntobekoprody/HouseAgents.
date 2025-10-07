package za.co.fittracksa.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface OfflineQueueDao {
    @Query("SELECT * FROM pending_activity")
    fun pendingActivities(): Flow<List<PendingActivityEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertActivity(entity: PendingActivityEntity)

    @Query("DELETE FROM pending_activity WHERE id = :id")
    suspend fun deleteActivity(id: Int)

    @Query("SELECT * FROM pending_meal")
    fun pendingMeals(): Flow<List<PendingMealEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMeal(entity: PendingMealEntity)

    @Query("DELETE FROM pending_meal WHERE id = :id")
    suspend fun deleteMeal(id: Int)
}
