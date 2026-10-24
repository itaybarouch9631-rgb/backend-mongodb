from types import SimpleNamespace

from bson import ObjectId
from services.tasks import delete_task_by_id, update_task_by_id


def test_delete_task_filters_by_owner(monkeypatch):
    task_id = "507f1f77bcf86cd799439011"
    user_id = "user-b"
    captured = {}

    class FakeTasksCollection:
        def delete_one(self, query):
            captured["query"] = query

            # Simulate that no document matched the query
            return SimpleNamespace(deleted_count=0)

    monkeypatch.setattr(
        "services.tasks.tasks_collection",
        FakeTasksCollection(),
    )

    result = delete_task_by_id(task_id, user_id)

    assert result is False

    assert captured["query"] == {
        "_id": ObjectId(task_id),
        "user_id": user_id,
    }


def test_update_task_filters_by_owner(monkeypatch):
    task_id = "507f1f77bcf86cd799439011"
    user_id = "user-b"
    update_data = {"title": "Updated title"}
    captured = {}

    class FakeTasksCollection:
        def update_one(self, query, update):
            captured["query"] = query
            captured["update"] = update

            return SimpleNamespace(matched_count=0)

    monkeypatch.setattr(
        "services.tasks.tasks_collection",
        FakeTasksCollection(),
    )
    
    result = update_task_by_id(task_id, user_id, update_data)

    assert result is None

    assert captured["query"] == {
        "_id": ObjectId(task_id),
        "user_id": user_id,
    }

    assert captured["update"] == {
        "$set": update_data,
    }