from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    nome_usuario: str
    email: EmailStr
    telefone: str
    senha: str

    @field_validator("senha")
    @classmethod
    def senha_minima(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres")
        return value


class UserLoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    welcome_message: str = ""
    contacts: list = []