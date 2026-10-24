from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers.tasks import router as tasks_router
from routers.users import router as users_router 

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks")
app.include_router(users_router, prefix="/users")