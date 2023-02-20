from pydantic import BaseModel


class BaseDto(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_mutation = False
        use_enum_values = True
        orm_mode = True
