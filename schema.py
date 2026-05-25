from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    
class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: bool

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime|None = None

    model_config = ConfigDict(from_attributes=True)
