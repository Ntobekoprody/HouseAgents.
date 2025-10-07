from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .auth import get_current_token_payload
from .database import Base, engine, get_session
from .models import User
from .schemas import (
    TokenPayload,
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

app = FastAPI(title="FitTrack SA API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/register", response_model=UserRead, tags=["auth"], status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
    return await crud.register_user(session, payload)


@app.post("/auth/login", response_model=Token, tags=["auth"])
async def login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> Token:
    return await crud.login_user(session, payload)


@app.post("/auth/google", response_model=Token, tags=["auth"])
async def google_login(payload: GoogleSSORequest, session: AsyncSession = Depends(get_session)) -> Token:
    return await crud.login_with_google(session, payload)


async def _get_current_user(
    token_payload: TokenPayload = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await crud.get_user_by_id(session, int(token_payload.sub))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.get("/me", response_model=UserRead, tags=["users"])
async def read_profile(user: User = Depends(_get_current_user)) -> UserRead:
    return UserRead.from_orm(user)


@app.get("/activities", response_model=list[ActivityRead], tags=["activities"])
async def get_activities(user: User = Depends(_get_current_user), session: AsyncSession = Depends(get_session)) -> list[ActivityRead]:
    return await crud.list_activities(session, user)


@app.post("/activities", response_model=ActivityRead, status_code=status.HTTP_201_CREATED, tags=["activities"])
async def post_activity(
    payload: ActivityCreate,
    user: User = Depends(_get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ActivityRead:
    return await crud.create_activity(session, user, payload)


@app.get("/nutrition", response_model=list[NutritionRead], tags=["nutrition"])
async def get_nutrition(user: User = Depends(_get_current_user), session: AsyncSession = Depends(get_session)) -> list[NutritionRead]:
    return await crud.list_nutrition(session, user)


@app.post("/nutrition", response_model=NutritionRead, status_code=status.HTTP_201_CREATED, tags=["nutrition"])
async def post_nutrition(
    payload: NutritionCreate,
    user: User = Depends(_get_current_user),
    session: AsyncSession = Depends(get_session),
) -> NutritionRead:
    return await crud.create_nutrition(session, user, payload)


@app.get("/achievements", tags=["gamification"])
async def get_achievements(
    user: User = Depends(_get_current_user), session: AsyncSession = Depends(get_session)
) -> list[dict]:
    achievements = await crud.list_achievements(session, user)
    return [
        {
            "id": achievement.id,
            "badge_name": achievement.badge_name,
            "description": achievement.description,
            "achieved_at": achievement.achieved_at,
        }
        for achievement in achievements
    ]


@app.get("/settings", response_model=SettingsRead, tags=["settings"])
async def get_settings(user: User = Depends(_get_current_user), session: AsyncSession = Depends(get_session)) -> SettingsRead:
    return await crud.read_settings(session, user)


@app.patch("/settings", response_model=SettingsRead, tags=["settings"])
async def patch_settings(
    payload: SettingsUpdate,
    user: User = Depends(_get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SettingsRead:
    return await crud.update_settings(session, user, payload)
