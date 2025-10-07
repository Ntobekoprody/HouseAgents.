# FitTrack SA Prototype Repository

This repository contains the planning artefacts, FastAPI backend prototype, automated tests, and CI configuration for the FitTrack SA mobile fitness application. The goal is to demonstrate an end-to-end slice of the product: secure authentication (including Google SSO), activity and nutrition logging, gamified achievements, and persistent user settings that reflect the South African context described in the product brief.

## Repository Structure

```
backend/        # FastAPI service implementation and tests
  app/
  tests/
docs/           # Product design and planning documentation
mobile/         # Kotlin/Jetpack Compose prototype scaffolding (see below)
.github/workflows/ # GitHub Actions configuration
```

## Getting Started

You can either download the project as a ZIP archive from GitHub or clone it with Git:

```bash
# Option A: download the repository ZIP from GitHub and extract it locally

# Option B: clone via Git
git clone https://github.com/<your-account>/FitTrack-SA.git
cd FitTrack-SA
```

Once the files are on your machine follow the steps below to run the backend API and, optionally, the Android client.

## Backend Prototype

The backend is built with FastAPI and SQLAlchemy using an async SQLite database (ready to upgrade to PostgreSQL for hosting). Features include:

- `POST /register`: email/password sign-up with hashed passwords.
- `POST /auth/login`: email/password login returning a JWT.
- `POST /auth/google`: Google SSO login with ID token verification (requires `GOOGLE_CLIENT_ID`).
- Authenticated CRUD for activities, nutrition entries, achievements, and settings.
- Gamification badges awarded for significant workouts and consistent nutrition logging.

### Running Locally

#### Requirements
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) **or** a virtual environment with `pip`

#### Setup with Poetry (recommended)
1. `cd backend`
2. `poetry install`
3. `poetry run uvicorn app.main:app --reload`
4. Visit `http://localhost:8000/docs` to exercise the REST endpoints.

#### Setup with pip
1. `cd backend`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`
5. Open `http://localhost:8000/docs`

> **SSO configuration**: Set `GOOGLE_CLIENT_ID` in the environment (or `.env`) to enable Google Sign-In token verification. Without the variable the API returns `503` for the SSO endpoint, keeping tests deterministic.

### Automated Tests

```
cd backend
# if you used Poetry
poetry run pytest
# if you used pip
pytest
```

The suite registers users, exercises the activity/nutrition flows, and validates settings updates and badge awarding.

## Mobile Prototype (Kotlin/Jetpack Compose)

The `mobile/` folder documents the Android app architecture and supplies starter Kotlin modules (view models, repositories, Retrofit clients, Room entities) to integrate with this backend. The Compose UI scaffolding includes the following screens:

- Onboarding & authentication (email + Google SSO placeholder).
- Dashboard summarising steps, calories, hydration reminders, and weekly challenges.
- Activity and Nutrition logging forms with offline caching using Room.
- Achievements carousel and progress charts.
- Settings with bilingual language toggle (English/isiZulu) and notification switches.

See `mobile/README.md` for details on building the Android module inside Android Studio.

### Quickstart (Android Studio)
1. Install [Android Studio Iguana or newer](https://developer.android.com/studio).
2. From the Android Studio welcome screen choose **Open**, navigate to the repository root, and select it.
3. Android Studio uses the bundled wrapper scripts under `mobile/` to download Gradle 8.4 and the Android Gradle Plugin the first time you sync. If you need to override the backend URL, set `FITTRACK_BASE_URL` in `local.properties`.
4. Connect an Android device or start an emulator, then press **Run ▶** on the `app` configuration.
5. Sign up with email/password via the backend running locally (or your hosted instance). Google SSO becomes available once you supply a valid `google-services.json`.

> **Command-line builds**: Run `cd mobile && ./gradlew tasks` (macOS/Linux/Git Bash) or `cd mobile && .\gradlew.bat tasks` (Windows PowerShell/CMD). The scripts download Gradle on first run and cache it under `mobile/.gradle/` if `GRADLE_USER_HOME` is not already set.

## Documentation

- `docs/design.md` summarises the personas, requirements, IA, data model, and 10-week roadmap.
- Additional implementation notes for deployment, API hosting, and testing should be recorded alongside development.

## GitHub Actions

Automated tests run on every push via the workflow defined in `.github/workflows/backend.yml`. The workflow installs dependencies, runs the FastAPI test suite, and surfaces coverage for the CI/CD rubric.

## Next Steps

- Deploy the FastAPI service to Render/Azure or Firebase Hosting with Cloud Run.
- Hook Retrofit clients in the Android app to the hosted API and finalise Room synchronisation.
- Implement biometric authentication using Android's BiometricPrompt.
- Extend gamification with weekly challenges and community leaderboards.

## Licence

This project is released under the MIT Licence.
