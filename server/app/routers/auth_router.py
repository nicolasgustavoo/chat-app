from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastro de novo usuário",
    response_description="Usuário cadastrado com sucesso",
)
def cadastrar(
    data: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Cadastra um novo usuário no sistema.

    - **usuario**: nome de usuário único
    - **email**: e-mail único e válido
    - **telefone**: telefone no formato (XX) XXXXX-XXXX
    - **senha**: mínimo 6 caracteres
    """
    service = AuthService(db)
    return service.cadastrar(data)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    summary="Login de usuário",
    response_description="Token JWT gerado com sucesso",
)
def login(
    data: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Autentica um usuário e retorna um token JWT.

    - **email**: e-mail cadastrado
    - **senha**: senha do usuário
    """
    service = AuthService(db)
    return service.login(data)


@router.delete(
    "/test/cleanup",
    status_code=status.HTTP_200_OK,
    summary="Limpa banco de dados de teste",
    include_in_schema=False,
)
def cleanup(db: Session = Depends(get_db)) -> dict:
    """Endpoint exclusivo para testes — remove todos os usuários do banco."""
    from app.models.user import UserModel
    import os
    if os.getenv("ENVIRONMENT") != "production":
        db.query(UserModel).delete()
        db.commit()
        return {"message": "Banco limpo com sucesso"}