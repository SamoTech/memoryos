from pydantic import BaseModel


class TagRead(BaseModel):
    id: str
    name: str
    color: str
    memory_count: int

    model_config = {"from_attributes": True}
