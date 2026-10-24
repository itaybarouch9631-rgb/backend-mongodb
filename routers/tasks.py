from fastapi import APIRouter, HTTPException, Query, Depends
from security import get_current_user
from schemas import TaskCreate, TaskUpdate
from bson.errors import InvalidId
from services.tasks import (
    create_task, 
    get_tasks,
    get_task_by_id,
    update_task_by_id,    
    delete_task_by_id
)

router = APIRouter()


@router.post("/")
def add_task(
    task: TaskCreate,
    user_id: str = Depends(get_current_user)        
):
    task_data = task.model_dump()
    task_data["user_id"] = user_id
    
    return create_task(task_data)


@router.get("/")
def read_tasks(
    completed: bool | None = None,
    category: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, le=100),
    user_id: str = Depends(get_current_user),    
):
       return get_tasks(
        user_id=user_id,
        completed=completed,
        category=category,
        search=search,
        page=page,
        limit=limit
    )

@router.get("/{task_id}")
def read_task(
    task_id: str,
    user_id: str = Depends(get_current_user)    
):
    try:
        task = get_task_by_id(task_id, user_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID format"
        )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found" 
        )
    
    return task


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    task: TaskUpdate,
    user_id: str = Depends(get_current_user)                           
):
    update_data = task.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
        status_code=400,
        detail="No fields provided for update"
        )

    try:
        updated_task = update_task_by_id(
            task_id,
            user_id,
            update_data
        )
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID format"
        )
    
    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task



@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user)    
):
    try:
        deleted = delete_task_by_id(task_id, user_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID format"
        )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}
