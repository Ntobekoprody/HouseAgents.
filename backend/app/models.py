from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    google_sub: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    biometrics_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    activities: Mapped[list[Activity]] = relationship("Activity", back_populates="user")
    meals: Mapped[list[Nutrition]] = relationship("Nutrition", back_populates="user")
    achievements: Mapped[list[Achievement]] = relationship("Achievement", back_populates="user")
    settings: Mapped[UserSettings] = relationship(
        "UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class ActivityType(str, Enum):
    WALKING = "walking"
    RUNNING = "running"
    CYCLING = "cycling"
    CUSTOM = "custom"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String, default=ActivityType.WALKING.value)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    calories_burned: Mapped[int] = mapped_column(Integer)
    steps: Mapped[int | None] = mapped_column(Integer)
    perceived_effort: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="activities")


class Nutrition(Base):
    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    food_item: Mapped[str] = mapped_column(String)
    calories: Mapped[int] = mapped_column(Integer)
    meal_type: Mapped[str | None] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="meals")


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    badge_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    achieved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="achievements")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    language: Mapped[str] = mapped_column(String, default="en")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    hydration_reminders: Mapped[bool] = mapped_column(Boolean, default=True)
    timezone: Mapped[str | None] = mapped_column(String, default="Africa/Johannesburg")

    user: Mapped[User] = relationship("User", back_populates="settings")
