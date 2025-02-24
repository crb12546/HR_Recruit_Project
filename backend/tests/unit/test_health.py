import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
