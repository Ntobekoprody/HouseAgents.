package za.co.fittracksa.di

import android.app.Application
import androidx.room.Room
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import za.co.fittracksa.data.api.FitTrackApi
import za.co.fittracksa.data.local.FitTrackDatabase
import za.co.fittracksa.domain.ActivityRepository
import za.co.fittracksa.domain.AuthRepository
import za.co.fittracksa.domain.NutritionRepository
import za.co.fittracksa.domain.SettingsRepository
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        val contentType = "application/json".toMediaType()
        val json = Json { ignoreUnknownKeys = true }
        return Retrofit.Builder()
            .baseUrl("https://api.example.com")
            .client(OkHttpClient())
            .addConverterFactory(json.asConverterFactory(contentType))
            .build()
    }

    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): FitTrackApi = retrofit.create(FitTrackApi::class.java)

    @Provides
    @Singleton
    fun provideDatabase(app: Application): FitTrackDatabase =
        Room.databaseBuilder(app, FitTrackDatabase::class.java, "fittrack.db").fallbackToDestructiveMigration().build()

    @Provides
    fun provideOfflineDao(db: FitTrackDatabase) = db.offlineQueueDao()

    @Provides
    fun provideAuthRepository(api: FitTrackApi) = AuthRepository(api)

    @Provides
    fun provideActivityRepository(api: FitTrackApi, db: FitTrackDatabase) =
        ActivityRepository(api, db.offlineQueueDao())

    @Provides
    fun provideNutritionRepository(api: FitTrackApi, db: FitTrackDatabase) =
        NutritionRepository(api, db.offlineQueueDao())

    @Provides
    fun provideSettingsRepository(api: FitTrackApi) = SettingsRepository(api)
}
