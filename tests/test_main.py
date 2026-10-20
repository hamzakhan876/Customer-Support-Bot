from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_refund_question():
    response = client.post(
        "/chat",
        json={"message": "When will I receive my refund?"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["intent"] == "refund_status"
    assert data["source"] == "KB003"
    assert data["resolved"] is True


def test_unknown_question_uses_fallback():
    response = client.post(
        "/chat",
        json={"message": "Can you recommend a laptop?"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["intent"] == "unknown"
    assert data["source"] is None
    assert data["resolved"] is False


def test_empty_message_is_rejected():
    response = client.post(
        "/chat",
        json={"message": ""},
    )

    assert response.status_code == 422

    
def test_track_order_question():
    response = client.post(
        "/chat",
        json={"message": "How can I track my order?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "track_order"
    assert data["source"] == "KB001"
    assert data["resolved"] is True


def test_return_policy_question():
    response = client.post(
        "/chat",
        json={"message": "How can I return an item?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "return_policy"
    assert data["source"] == "KB002"
    assert data["resolved"] is True


def test_message_over_maximum_length_is_rejected():
    response = client.post(
        "/chat",
        json={"message": "a" * 2001},
    )

    assert response.status_code == 422
