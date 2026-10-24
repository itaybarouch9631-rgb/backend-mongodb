from fastapi.testclient import TestClient
from main import app
from security import create_access_token

client = TestClient(app)


def test_get_tasks_without_token_is_rejected():
    response = client.get("/tasks/")

    assert response.status_code in (401, 403)


def test_get_tasks_with_invalid_token_is_rejected():
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_get_tasks_with_valid_token_is_allowed():
    token = create_access_token("test-user-id")

    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200


def test_get_tasks_filters_by_current_user(monkeypatch):
    captured = {}

    def fake_get_tasks(
        user_id,
        completed,
        category,
        search,
        page,
        limit
    ):
        captured["user_id"] = user_id
        return []

    monkeypatch.setattr(
        "routers.tasks.get_tasks",
        fake_get_tasks
    )

    token = create_access_token("test-user-id")

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert captured["user_id"] == "test-user-id"


def test_cannot_get_another_users_task(monkeypatch):
    task_id = "507f1f77bcf86cd799439011"
    captured = {}

    def fake_get_task_by_id(task_id_arg, user_id):
        captured["user_id"] = user_id
        return None

    monkeypatch.setattr(
        "routers.tasks.get_task_by_id",
        fake_get_task_by_id,
    )

    token = create_access_token("test-user-id")

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert captured["user_id"] == "test-user-id"


def test_cannot_update_another_users_task(monkeypatch):
    task_id = "507f1f77bcf86cd799439011"
    captured = {}

    def fake_update_task_by_id(
        task_id_arg,
        user_id,
        update_data,
    ):
        captured["user_id"] = user_id
        captured["update_data"] = update_data.copy()
        return None

    monkeypatch.setattr(
        "routers.tasks.update_task_by_id",
        fake_update_task_by_id,
    )

    token = create_access_token("test-user-id")

    response = client.patch(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated title"},
    )

    assert response.status_code == 404
    assert captured["user_id"] == "test-user-id"
    assert captured["update_data"] == {
        "title": "Updated title"
    }


def test_cannot_delete_another_users_task(monkeypatch):
    task_id = "507f1f77bcf86cd799439011"
    captured = {}

    def fake_delete_task_by_id(task_id_arg, user_id):
        captured["task_id"] = task_id_arg
        captured["user_id"] = user_id
        return False

    monkeypatch.setattr(
        "routers.tasks.delete_task_by_id",
        fake_delete_task_by_id,
    )

    token = create_access_token("test-user-id")

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
