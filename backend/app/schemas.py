from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleSSORequest(BaseModel):
    id_token: str


class ActivityBase(BaseModel):
    type: str = Field(default="walking", examples=["walking", "running", "cycling", "custom"])
    duration_minutes: int = Field(gt=0)
    calories_burned: int = Field(ge=0)
    steps: Optional[int] = Field(default=None, ge=0)
    perceived_effort: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = Field(default=None, max_length=500)
    timestamp: Optional[datetime] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class NutritionBase(BaseModel):
    food_item: str
    calories: int = Field(ge=0)
    meal_type: Optional[str] = Field(default=None, max_length=50)
    timestamp: Optional[datetime] = None


class NutritionCreate(NutritionBase):
    pass


class NutritionRead(NutritionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class AchievementRead(BaseModel):
    id: int
    badge_name: str
    description: str
    achieved_at: datetime

    class Config:
        orm_mode = True


class SettingsUpdate(BaseModel):
    language: Optional[str] = Field(default=None)
    notifications_enabled: Optional[bool] = None
    hydration_reminders: Optional[bool] = None
    timezone: Optional[str] = None


class SettingsRead(BaseModel):
    language: str
    notifications_enabled: bool
    hydration_reminders: bool
    timezone: Optional[str]

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: Optional[str]
    biometrics_enabled: bool

    class Config:
        orm_mode = True
