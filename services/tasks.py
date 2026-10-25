from database import tasks_collection
from bson import ObjectId

def serialize_task(task: dict | None) -> dict | None:
    if task is None:
        return None

    task["_id"] = str(task["_id"])
    return task

def create_task(task_data: dict):
    result = tasks_collection.insert_one(task_data)

    return {
        "id": str(result.inserted_id),
        "message": "Task created successfully"
    }



def get_tasks(
    user_id: str,
    completed: bool | None = None,
    category: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10
):
    query = {"user_id": user_id}

    if completed is not None:
        query["completed"] = completed

    if category is not None:
        query["category"] = category

    if search is not None:
        query["title"] = {
            "$regex": search,
            "$options": "i"
        }

    skip = (page - 1) * limit

    tasks = list(
        tasks_collection.find(query)
        .sort("priority", -1)
        .skip(skip)
        .limit(limit)
    )

    return [serialize_task(task) for task in tasks]



def get_task_by_id(task_id: str, user_id: str):
    object_id = ObjectId(task_id)
    
    task = tasks_collection.find_one({
        "_id": object_id,
        "user_id": user_id
        })

    if task is None:
        return None

    return serialize_task(task)

def update_task_by_id(
    task_id: str,
    user_id: str,
    update_data: dict
):
    object_id = ObjectId(task_id)

    result = tasks_collection.update_one(
        {
            "_id": object_id,
            "user_id": user_id
        },
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    task = tasks_collection.find_one({
        "_id": object_id,
        "user_id": user_id
    })

    return serialize_task(task)


def delete_task_by_id(task_id: str, user_id: str):
    object_id = ObjectId(task_id)

    result = tasks_collection.delete_one({
        "_id": object_id,
        "user_id": user_id            
    })

    return result.deleted_count > 0