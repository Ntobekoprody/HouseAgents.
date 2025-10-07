package za.co.fittracksa.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val lightColors = lightColorScheme()
private val darkColors = darkColorScheme()

@Composable
fun FitTrackTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = lightColors,
        typography = androidx.compose.material3.Typography(),
        content = content,
    )
}
