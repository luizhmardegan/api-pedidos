from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from jose import jwt
from datetime import datetime, timedelta, timezone
import bcrypt

# Cria router de autenticação
auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Função usada para criar token JWT para usuário
def criar_token(
    id_usuario, duracao_token=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


# Função usada para validar se existe usuário cadastrado com essas credenciais
def autenticar_usuario(email, senha, session):
    # Busca usuário com email informado
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    # Não encontrou usuário com e-mail
    if not usuario:
        return False

    # Converte senha enviada pelo usuário para Bytes
    senha_bytes = senha.encode("utf-8")

    # A senha do usuário do banco não confere com senha enviada
    if not bcrypt.checkpw(senha_bytes, usuario.senha):
        return False

    # Se chegou aqui é porque usuário existe
    return usuario


@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return {"mensagem": "Acessou a rota padrão de autenticação"}


@auth_router.post("/criar_conta")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)
):
    """
    Rota para cadastrar um novo usuário
    """
    usuario = (
        session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    )

    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        pwd_bytes = usuario_schema.senha.encode("utf-8")
        salt = bcrypt.gensalt()
        senha_criptografada = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        novo_usuario = Usuario(
            usuario_schema.nome,
            usuario_schema.email,
            senha_criptografada,
            usuario_schema.ativo,
            usuario_schema.admin,
        )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso: {usuario_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """
    Rota para realizar login de usuário
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(
            status_code=400, detail="Usuário não encontrado ou credenciais inválidas"
        )
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@auth_router.post("/login-form")
async def login_form(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(pegar_sessao),
):
    """
    Rota para realizar login no botão "Authorize" no Swagger
    """
    usuario = autenticar_usuario(
        dados_formulario.username, dados_formulario.password, session
    )

    if not usuario:
        raise HTTPException(
            status_code=400, detail="Usuário não encontrado ou credenciais inválidas"
        )
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "Bearer"}
