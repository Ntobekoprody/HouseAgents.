# FitTrack SA Android Prototype

This directory contains Kotlin scaffolding and architecture notes for the FitTrack SA Android application. The goal is to demonstrate how the app integrates with the FastAPI backend, supports offline-first data capture, and surfaces the core UX journeys described in the product brief.

## Tech Stack
- **Jetpack Compose** for UI.
- **Hilt** for dependency injection.
- **Retrofit + Kotlin Serialization** for REST API integration.
- **Room** for offline caching and synchronisation queues.
- **AndroidX DataStore** for lightweight settings persistence (language, notifications, biometrics).
- **Google Identity Services** for SSO.

## Module Outline
```
mobile/
  app/
    build.gradle.kts
    src/main/java/za/co/fittracksa/
      FitTrackApp.kt
      di/
      data/
      domain/
      ui/
```

The source tree includes view models, repositories, and Compose screens that illustrate the navigation and state management strategy. The module is intentionally minimal so it can be imported into Android Studio and extended during the prototype sprint.

## Environment Variables
Create a `local.properties` entry or Gradle `resValue` for `FITTRACK_BASE_URL` pointing to the hosted FastAPI instance. Google SSO requires a `google-services.json` file configured for the package `za.co.fittracksa`.

## Running the App
1. Open the `mobile` project root in Android Studio Iguana or newer.
2. When prompted, let Android Studio download the Gradle wrapper and Android Gradle Plugin dependencies (the project is configured for AGP 8.3.2 / Gradle 8.6).
3. Use the "app" run configuration to launch on an emulator or device.
4. Create a test account via email/password or login with Google SSO once configured.

The prototype currently focuses on UI and data flows rather than polished visuals. Wireframes and copy can be updated based on pilot feedback.
