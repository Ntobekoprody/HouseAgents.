
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # ensure startup event runs to create tables
    with TestClient(app) as client:
        client.get("/health")
        yield


def test_register_and_login_roundtrip():
    with TestClient(app) as client:
        payload = {"email": "user@example.com", "password": "Password123!"}
        response = client.post("/register", json=payload)
        assert response.status_code == 201, response.text

        login_response = client.post("/auth/login", json=payload)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        me_response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
        assert me_response.status_code == 200
        data = me_response.json()
        assert data["email"] == payload["email"]


def test_activity_and_nutrition_flow():
    with TestClient(app) as client:
        payload = {"email": "flow@example.com", "password": "Password123!"}
        client.post("/register", json=payload)
        token = client.post("/auth/login", json=payload).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        activity_payload = {
            "type": "running",
            "duration_minutes": 45,
            "calories_burned": 350,
            "steps": 6000,
            "perceived_effort": "moderate",
        }
        activity_response = client.post("/activities", json=activity_payload, headers=headers)
        assert activity_response.status_code == 201
        activity_data = activity_response.json()
        assert activity_data["type"] == "running"

        nutrition_payload = {
            "food_item": "Pap and chakalaka",
            "calories": 550,
            "meal_type": "lunch",
        }
        nutrition_response = client.post("/nutrition", json=nutrition_payload, headers=headers)
        assert nutrition_response.status_code == 201

        achievements_response = client.get("/achievements", headers=headers)
        assert achievements_response.status_code == 200
        badges = achievements_response.json()
        assert any(badge["badge_name"] == "30-Minute Hero" for badge in badges)
        assert any(badge["badge_name"] == "Step Starter" for badge in badges)

        settings_response = client.get("/settings", headers=headers)
        assert settings_response.status_code == 200
        assert settings_response.json()["language"] == "en"

        update_payload = {"language": "zu", "notifications_enabled": False}
        patch_response = client.patch("/settings", json=update_payload, headers=headers)
        assert patch_response.status_code == 200
        assert patch_response.json()["language"] == "zu"
