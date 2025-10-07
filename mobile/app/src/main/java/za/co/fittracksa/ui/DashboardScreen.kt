package za.co.fittracksa.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun DashboardScreen(
    state: DashboardState,
    onLogActivity: () -> Unit,
    onLogMeal: () -> Unit,
    onViewAchievements: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(
            text = "Sanibonani!",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
        )

        StatCard(title = "Steps", value = "${state.steps}")
        StatCard(title = "Calories", value = "${state.calories} kcal")
        StatCard(title = "Streak", value = "${state.streakDays} days")
        ReminderCard(state)

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
            Button(onClick = onLogActivity, modifier = Modifier.weight(1f)) {
                Text("Log Activity")
            }
            Button(onClick = onLogMeal, modifier = Modifier.weight(1f)) {
                Text("Log Meal")
            }
        }

        Button(onClick = onViewAchievements, modifier = Modifier.fillMaxWidth()) {
            Text("View Achievements")
        }
    }
}

@Composable
private fun StatCard(title: String, value: String) {
    Card(colors = CardDefaults.cardColors(), modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = title, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
            Text(text = value, style = MaterialTheme.typography.headlineSmall)
        }
    }
}

@Composable
private fun ReminderCard(state: DashboardState) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(text = "Hydration Reminder", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold)
            val hydrationText = if (state.hydrationReminder) "Remember to drink water every hour." else "Hydration reminders off"
            Text(text = hydrationText, style = MaterialTheme.typography.bodySmall)
            Text(text = "Weekly Challenge: ${state.weeklyChallenge}", style = MaterialTheme.typography.bodySmall)
        }
    }
}

data class DashboardState(
    val steps: Int,
    val calories: Int,
    val hydrationReminder: Boolean,
    val weeklyChallenge: String,
    val streakDays: Int,
)
