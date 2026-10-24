from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5)
    category: str = Field(min_length=1, max_length=50)
    completed: bool = False


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=100)
    priority: int | None = Field(default=None, ge=1, le=5)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    completed: bool | None = None   


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str
    password: str = Field(min_length=8)    


class UserLogin(BaseModel):
    username: str
    password: str