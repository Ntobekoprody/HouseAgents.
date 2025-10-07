package za.co.fittracksa.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            FitTrackTheme {
                FitTrackAppShell()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FitTrackAppShell() {
    val title by remember { mutableStateOf("FitTrack SA") }
    Scaffold(topBar = { TopAppBar(title = { Text(text = title) }) }) { padding ->
        Surface(modifier = Modifier, color = MaterialTheme.colorScheme.background) {
            DashboardPreview()
        }
    }
}

@Composable
fun DashboardPreview() {
    DashboardScreen(
        state = DashboardState(
            steps = 7500,
            calories = 520,
            hydrationReminder = true,
            weeklyChallenge = "Log three workouts",
            streakDays = 4,
        ),
        onLogActivity = {},
        onLogMeal = {},
        onViewAchievements = {},
    )
}
