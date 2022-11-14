from pydantic import BaseModel

from models import Gender, Role


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str | None
    gender: Gender
    role: Role

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user_id: int | None
    first_name: str | None
    last_name: str | None
    gender: Gender | None
    role: Role | None

    class Config:
        orm_mode = True
        
class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    gender: Gender | None
    role: Role | None
    
    class Config:
        orm_mode = True