from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Criar aplicação FastAPI
app = FastAPI()

# Define schema de autentição da página Swagger
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from routes.auth import auth_router
from routes.order import order_router

app.include_router(auth_router)
app.include_router(order_router)
