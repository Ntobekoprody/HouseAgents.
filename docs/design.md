# FitTrack SA Prototype Plan

## Overview
FitTrack SA is a bilingual (English and isiZulu), ad-free fitness and wellness tracker designed for South African users who need an inclusive experience that works even when connectivity is intermittent. The product vision unifies activity, nutrition and motivation features into a lightweight Android app powered by a secure REST API.

## Goals
- Deliver a prototype that demonstrates the full authentication journey: email/password registration, Google SSO and biometric opt-in.
- Support activity and nutrition tracking, including offline capture with delayed synchronisation.
- Provide community-inspired gamification (badges, streaks, challenges) to sustain motivation.
- Respect usability, accessibility and cultural relevance for South African audiences.

## Personas & Journeys
1. **Nomsa – Busy Nurse**: Wants quick logging between shifts, relies on offline capture during commutes, prefers isiZulu UI, values hydration reminders.
2. **David – University Student**: Uses Google account for SSO, competes with friends, responds well to weekly challenges and streak tracking.
3. **Lerato – Returning to Fitness**: Needs gentle prompts, simple nutrition logging for local meals, offline-first design for limited data bundles.

High-level journeys: onboarding (register/login → profile setup → language selection), daily engagement (dashboard → log activity/nutrition → review achievements), retention (receive notifications → re-engage via streak summaries and weekly challenge alerts).

## Feature Breakdown
| Epic | Key Features | Notes |
| --- | --- | --- |
| Authentication | Email registration, login, Google SSO, biometric toggle | Uses JWT tokens from backend, biometrics handled on-device via Android BiometricPrompt. |
| Activity Tracking | Manual logging, automatic step sync placeholder, view history | Backend calculates gamification triggers. |
| Nutrition Tracking | Meal logging with SA-centric presets, offline queue | Utilises Room database for offline caching. |
| Gamification | Badges, streak counter, weekly challenge metadata | Calculated server-side with scheduled jobs. |
| Notifications | Hydration, activity, nutrition reminders | Firebase Cloud Messaging integration planned. |
| Settings | Language toggle (en/zu), notifications, biometric switch | Synced to backend for cross-device consistency. |

## Information Architecture
- **Bottom Navigation**: Dashboard, Activity, Nutrition, Progress, Settings.
- **Dashboard Widgets**: Daily steps, calories burned, meal summary, active streak, next challenge, offline sync status.
- **Activity Flow**: List → Activity detail → Log/edit activity → Summary charts.
- **Nutrition Flow**: Daily meals list → Add meal (search database, quick add, custom meal) → Macro summary.
- **Progress Screens**: Weekly and monthly charts for activity and nutrition, achievements timeline.
- **Settings**: Language toggle, notification switches, biometric toggle, account management, connected devices (future).

## UI Patterns
- Material 3 theming with accessible contrast ratios.
- Typography uses Google Noto Sans to support isiZulu characters.
- Offline mode banner persists until sync completes.
- Gamification badges displayed in card carousel.

## API Design Summary
The FastAPI backend exposes:
- `POST /register`, `POST /auth/login`, `POST /auth/google` for authentication.
- Authenticated endpoints for activities, nutrition, achievements and user settings using JWT bearer tokens.
- SQLite for rapid prototyping with SQLAlchemy ORM, ready to switch to PostgreSQL when hosted.
- Password hashing via `passlib`; Google SSO uses token verification with `google-auth`.
- Future extension: WebSocket channel for live challenge leaderboards.

## Data Model (simplified UML)
```
User "1" -- "*" Activity
User "1" -- "*" Nutrition
User "1" -- "*" Achievement
User "1" -- "1" UserSettings
```

**Entities**
- `User(id, email, passwordHash?, googleSub?, displayName?, biometricsEnabled, createdAt)`
- `Activity(id, userId, type, durationMinutes, caloriesBurned, steps?, perceivedEffort?, notes?, timestamp)`
- `Nutrition(id, userId, foodItem, calories, mealType?, timestamp)`
- `Achievement(id, userId, badgeName, description, achievedAt)`
- `UserSettings(id, userId, language, notificationsEnabled, hydrationReminders, timezone)`

## Offline Strategy
- Android app caches new entries in Room database tables mirroring backend schema.
- WorkManager job synchronises queued entries when the device regains connectivity.
- Sync conflict resolution favours the latest timestamp from device or server.

## Security & Privacy
- JWT-based auth tokens expire after 24 hours; refresh handled by silent login or SSO refresh token.
- Sensitive fields encrypted at rest on device using Android EncryptedSharedPreferences.
- All traffic enforced over HTTPS once deployed.
- Optional biometric unlock for convenience without storing biometrics on the backend.

## Project Plan (10 Weeks)
1. **Discovery (Weeks 1-2)**: Validate personas, refine requirements, finalise bilingual copy.
2. **Design (Weeks 3-4)**: Produce high-fidelity Figma screens, clickable prototype, review accessibility.
3. **Backend (Weeks 5-6)**: Build FastAPI service, integrate Google SSO, implement unit tests, containerise deployment.
4. **Android (Weeks 7-8)**: Develop Kotlin app using Jetpack Compose, integrate Retrofit, Room, Hilt, and DataStore.
5. **Stabilisation (Week 9)**: QA cycles, instrumentation tests, documentation, pilot feedback.
6. **Launch Prep (Week 10)**: Deploy backend to Render/Azure, configure CI/CD (GitHub Actions), conduct training session for pilot group.

## Risk Mitigation
- **Connectivity constraints** mitigated via offline-first design and efficient payloads.
- **SSO dependency** handled with graceful fallback to email login when Google services unavailable.
- **Cultural relevance** ensured through local food database curation and bilingual copy reviews.

## Success Metrics
- 80% weekly active retention during pilot.
- >60% of sessions include both activity and nutrition logging.
- Average response time < 300ms for API endpoints under pilot load.
- Positive user satisfaction (>4/5) on usability survey.
