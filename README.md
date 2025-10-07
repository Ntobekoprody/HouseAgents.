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

## Backend Prototype

The backend is built with FastAPI and SQLAlchemy using an async SQLite database (ready to upgrade to PostgreSQL for hosting). Features include:

- `POST /register`: email/password sign-up with hashed passwords.
- `POST /auth/login`: email/password login returning a JWT.
- `POST /auth/google`: Google SSO login with ID token verification (requires `GOOGLE_CLIENT_ID`).
- Authenticated CRUD for activities, nutrition entries, achievements, and settings.
- Gamification badges awarded for significant workouts and consistent nutrition logging.

### Running Locally

1. Install Poetry (or use `pipx install poetry`).
2. Install dependencies: `cd backend && poetry install`.
3. Start the API: `poetry run uvicorn app.main:app --reload`.
4. Access the interactive docs at `http://localhost:8000/docs`.

> **SSO configuration**: Set `GOOGLE_CLIENT_ID` in the environment (or `.env`) to enable Google Sign-In token verification. Without the variable the API returns `503` for the SSO endpoint, keeping tests deterministic.

### Automated Tests

```
cd backend
poetry run pytest
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
