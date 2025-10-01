from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker
from models import Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError


# Função usada para iniciar e encerrar sessão no banco de dados após cada operação
def pegar_sessao():
    try:
        # inicia sessão do banco de dados
        Session = sessionmaker(bind=db)
        session = Session()

        # retorna sessão do banco de dados
        yield session
    finally:
        # encerra sessão
        session.close()


# Função usada para verificar token e retornar usuário dono do token
def verificar_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)
):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Acesso Negado, verifique a validade do token"
        )

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario
