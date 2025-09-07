from app.app import app
import pytest


@pytest.mark.security
def test_csrf_protection(client):
    # Try posting to /add without CSRF token
    response = client.post("/add", data={"name": "malicious"})
    # Flask-WTF should reject it with 400 Bad Request
    assert response.status_code == 400
