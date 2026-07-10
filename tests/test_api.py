# This file contains pytest tests for FastAPI endpoints

import pytest
from fastapi.testclient import TestClient
import sys
import os

# add root and ml directory to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml")))

from api.main import app

client = TestClient(app)

# sample valid input for prediction
sample_input = {
    "Administrative": 0,
    "Administrative_Duration": 0.0,
    "Informational": 0,
    "Informational_Duration": 0.0,
    "ProductRelated": 1,
    "ProductRelated_Duration": 0.0,
    "BounceRates": 0.2,
    "ExitRates": 0.2,
    "PageValues": 0.0,
    "SpecialDay": 0.0,
    "Month": 2,
    "OperatingSystems": 1,
    "Browser": 1,
    "Region": 1,
    "TrafficType": 1,
    "VisitorType": 2,
    "Weekend": 0,
}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_valid_input():
    response = client.post("/predict", json=sample_input)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probability" in data
    assert "message" in data

    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_invalid_input():
    response = client.post("/predict", json={"Administrative": 0})

    assert response.status_code == 422


def test_predict_purchase_case():
    """
    Test prediction endpoint with a purchase-like input.

    This test verifies the API returns a valid prediction response.
    It does NOT assume the trained ML model will always predict class 1.
    """

    purchase_input = {
        "Administrative": 2,
        "Administrative_Duration": 80.0,
        "Informational": 1,
        "Informational_Duration": 25.0,
        "ProductRelated": 15,
        "ProductRelated_Duration": 450.0,
        "BounceRates": 0.02,
        "ExitRates": 0.05,
        "PageValues": 25.5,
        "SpecialDay": 0.0,
        "Month": 5,
        "OperatingSystems": 2,
        "Browser": 2,
        "Region": 1,
        "TrafficType": 2,
        "VisitorType": 2,
        "Weekend": 0,
    }

    response = client.post("/predict", json=purchase_input)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probability" in data
    assert "message" in data

    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert isinstance(data["message"], str)
