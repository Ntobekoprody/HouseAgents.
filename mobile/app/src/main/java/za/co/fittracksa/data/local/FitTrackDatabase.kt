package za.co.fittracksa.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [PendingActivityEntity::class, PendingMealEntity::class],
    version = 1,
    exportSchema = false,
)
abstract class FitTrackDatabase : RoomDatabase() {
    abstract fun offlineQueueDao(): OfflineQueueDao
}
