from pydantic import BaseModel

class ImageOut(BaseModel):
    id: int
    filename: str
    filepath: str
    content_type: str

    class Config:
        orm_mode = True