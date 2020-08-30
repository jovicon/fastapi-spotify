from typing import List

from pydantic import BaseModel

class ResultBase(BaseModel):
    search: str
    search_type: str
    result: dict


class ResultCreate(ResultBase):
    pass

class Result(ResultBase):
    id: int

    class Config:
        orm_mode = True