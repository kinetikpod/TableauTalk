from pydantic import BaseModel, EmailStr, Field


class SignupIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class SignupOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    access_token: str


class AuthOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    access_token: str


class VerifyEmailPayload(BaseModel):
    token: str


class SigninIn(BaseModel):
    email: EmailStr
    password: str


class SigninOut(BaseModel):
    id: int
    name: str
    email: EmailStr


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetOut(BaseModel):
    message: str


class MessageResponse(BaseModel):
    message: str


class PasswordResetInput(BaseModel):
    token: str
    new_password: str
