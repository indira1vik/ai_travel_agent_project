from pydantic import BaseModel, Field, EmailStr

class NewUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class AuthResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr