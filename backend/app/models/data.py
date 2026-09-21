from datetime import date

from pydantic import BaseModel, Field


class DataCreate(BaseModel):
    date: date
    value: float = Field(..., ge=0)
    memo: str = Field(default="", max_length=200)


class DataUpdate(BaseModel):
    date: date
    value: float = Field(..., ge=0)
    memo: str = Field(default="", max_length=200)


from datetime import date

from pydantic import BaseModel, Field


class DataCreate(BaseModel):
    date: date
    value: float = Field(..., ge=0)
    memo: str = Field(default="", max_length=200)


class DataUpdate(BaseModel):
    date: date
    value: float = Field(..., ge=0)
    memo: str = Field(default="", max_length=200)