from fastapi.testclient import TestClient

from cloudmesh_sentinel.main import app


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "cloudmesh-sentinel"}
