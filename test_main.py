from fastapi.testclient import TestClient
from api.main import app

#client app simulation
client = TestClient(app)

def test_audit_url_invalid():
    # Test with an invalid URL (no http/https)
    response = client.get("/api/audit", params={"url": "www.github.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "URL must begin with https:// or http://"}

def test_audit_url_non_html():
    #Test with non-HTML URL
    response = client.get("/api/audit", params={"url": "https://api.github.com"})
    assert response.status_code == 400
    assert response.json() == {"detail": "URL does not point to an HTML page"}

def test_audit_happy_path():
    #Test with happy path (valid HTML URL)
    response = client.get("/api/audit", params={"url": "https://www.github.com"})
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "meta_description" in data

