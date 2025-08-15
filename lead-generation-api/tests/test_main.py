"""
Basic tests for the FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Lead Generation AI"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"

def test_health_check():
    """Test basic health check"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

def test_detailed_health_check():
    """Test detailed health check"""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "dependencies" in data
    assert "timestamp" in data

def test_liveness_check():
    """Test liveness probe"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"

def test_unauthorized_access():
    """Test that protected endpoints require authentication"""
    response = client.post("/api/v1/leads/search", json={
        "main_query": "test query",
        "filters": {}
    })
    assert response.status_code == 401

def test_invalid_search_request():
    """Test invalid search request format"""
    # This will fail auth first, but tests the endpoint exists
    response = client.post("/api/v1/leads/search", json={
        "invalid": "data"
    })
    assert response.status_code in [401, 422]  # Auth or validation error