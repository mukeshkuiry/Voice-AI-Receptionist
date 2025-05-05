import pytest
import httpx
from flask import Flask
from main import app  # Replace with the actual filename without .py

@pytest.fixture
def test_client():
    app.config.update({
        "TESTING": True
    })
    return app.test_client()

def test_end_of_call_report(test_client):
    payload = {
        "message": {
            "type": "end-of-call-report",
            "callId": "abc123",
            "caller": {
                "name": "Test User",
                "phone": "+1111111111"
            },
            "duration": "5 minutes",
            "summary": "Test summary of the call.",
            "timestamp": "2025-05-05T12:00:00Z"
        }
    }

    response = test_client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert "Call report logged" in response.json.get("result", "")

def test_tool_call_email(test_client, monkeypatch):
    async def mock_send_email(to_email, subject, body):
        return True  # Pretend email sending always works

    from send_email import send_email
    monkeypatch.setattr("send_email.send_email", mock_send_email)

    payload = {
        "message": {
            "type": "tool-calls",
            "toolCalls": [
                {
                    "function": {
                        "arguments": {
                            "to_email": "test@example.com",
                            "subject": "Test Subject",
                            "body": "This is a test email body."
                        }
                    }
                }
            ]
        }
    }

    response = test_client.post("/tools/webhook", json=payload)
    assert response.status_code == 200
    assert "Your email has been sent" in response.json.get("result", "")
