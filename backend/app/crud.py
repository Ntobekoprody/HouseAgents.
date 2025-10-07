from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import create_access_token, get_password_hash, verify_password
from .config import get_settings
from .models import Achievement, Activity, Nutrition, User, UserSettings
from .schemas import (
    ActivityCreate,
    ActivityRead,
    GoogleSSORequest,
    NutritionCreate,
    NutritionRead,
    SettingsRead,
    SettingsUpdate,
    Token,
    UserCreate,
    UserLogin,
    UserRead,
)

settings = get_settings()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def ensure_settings(session: AsyncSession, user: User) -> UserSettings:
    if user.settings:
        return user.settings
    settings_obj = UserSettings(user_id=user.id)
    session.add(settings_obj)
    await session.flush()
    return settings_obj


async def register_user(session: AsyncSession, payload: UserCreate) -> UserRead:
    existing = await get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed = get_password_hash(payload.password)
    user = User(email=payload.email, password_hash=hashed, display_name=payload.display_name)
    session.add(user)
    await session.flush()
    await ensure_settings(session, user)
    await session.commit()
    await session.refresh(user)
    return UserRead.from_orm(user)


async def login_user(session: AsyncSession, payload: UserLogin) -> Token:
    user = await get_user_by_email(session, payload.email)
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(email=user.email, subject=str(user.id))
    return Token(access_token=token)


async def login_with_google(session: AsyncSession, payload: GoogleSSORequest) -> Token:
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google SSO is not configured",
        )
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.id_token,
            google_requests.Request(),
            settings.google_client_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token") from exc

    email = idinfo.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google account has no email")

    user = await get_user_by_email(session, email)
    if not user:
        user = User(email=email, google_sub=idinfo.get("sub"), display_name=idinfo.get("name"))
        session.add(user)
        await session.flush()
        await ensure_settings(session, user)
    else:
        user.google_sub = user.google_sub or idinfo.get("sub")
    await session.commit()
    token = create_access_token(email=user.email, subject=str(user.id))
    return Token(access_token=token)


async def create_activity(session: AsyncSession, user: User, payload: ActivityCreate) -> ActivityRead:
    activity = Activity(
        user_id=user.id,
        type=payload.type,
        duration_minutes=payload.duration_minutes,
        calories_burned=payload.calories_burned,
        steps=payload.steps,
        perceived_effort=payload.perceived_effort,
        notes=payload.notes,
        timestamp=payload.timestamp or datetime.utcnow(),
    )
    session.add(activity)
    await session.flush()
    await _update_achievements_for_activity(session, user, activity)
    await session.commit()
    await session.refresh(activity)
    return ActivityRead.from_orm(activity)


async def list_activities(session: AsyncSession, user: User) -> list[ActivityRead]:
    result = await session.execute(select(Activity).where(Activity.user_id == user.id).order_by(Activity.timestamp.desc()))
    activities = result.scalars().all()
    return [ActivityRead.from_orm(item) for item in activities]


async def create_nutrition(session: AsyncSession, user: User, payload: NutritionCreate) -> NutritionRead:
    meal = Nutrition(
        user_id=user.id,
        food_item=payload.food_item,
        calories=payload.calories,
        meal_type=payload.meal_type,
        timestamp=payload.timestamp or datetime.utcnow(),
    )
    session.add(meal)
    await session.flush()
    await _update_achievements_for_nutrition(session, user)
    await session.commit()
    await session.refresh(meal)
    return NutritionRead.from_orm(meal)


async def list_nutrition(session: AsyncSession, user: User) -> list[NutritionRead]:
    result = await session.execute(select(Nutrition).where(Nutrition.user_id == user.id).order_by(Nutrition.timestamp.desc()))
    meals = result.scalars().all()
    return [NutritionRead.from_orm(item) for item in meals]


async def list_achievements(session: AsyncSession, user: User) -> list[Achievement]:
    result = await session.execute(select(Achievement).where(Achievement.user_id == user.id))
    return result.scalars().all()


async def read_settings(session: AsyncSession, user: User) -> SettingsRead:
    settings_obj = await ensure_settings(session, user)
    return SettingsRead.from_orm(settings_obj)


async def update_settings(session: AsyncSession, user: User, payload: SettingsUpdate) -> SettingsRead:
    settings_obj = await ensure_settings(session, user)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(settings_obj, field, value)
    await session.commit()
    await session.refresh(settings_obj)
    return SettingsRead.from_orm(settings_obj)


async def _update_achievements_for_activity(session: AsyncSession, user: User, activity: Activity) -> None:
    await session.flush()
    if activity.duration_minutes >= 30:
        await _award_badge(session, user, "30-Minute Hero", "Completed a 30 minute activity")
    if activity.steps and activity.steps >= 5000:
        await _award_badge(session, user, "Step Starter", "Logged 5,000 steps in one activity")


async def _update_achievements_for_nutrition(session: AsyncSession, user: User) -> None:
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_meals = await session.execute(
        select(Nutrition).where(
            Nutrition.user_id == user.id,
            Nutrition.timestamp >= today_start,
        )
    )
    if len(today_meals.scalars().all()) >= 3:
        await _award_badge(session, user, "Consistent Logger", "Logged three meals today")


async def _award_badge(session: AsyncSession, user: User, badge_name: str, description: str) -> None:
    existing = await session.execute(
        select(Achievement).where(Achievement.user_id == user.id, Achievement.badge_name == badge_name)
    )
    if existing.scalar_one_or_none():
        return
    achievement = Achievement(user_id=user.id, badge_name=badge_name, description=description)
    session.add(achievement)
    await session.flush()
