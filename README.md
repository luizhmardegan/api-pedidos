API criada em Python com framework FastAPI. Simula o backend de um sistema de pedidos.

## Comandos úteis

**Criar ambiente virtual**
python virtualenv .venv

**Executar servidor**
uvicorn main:app --reload  
ou
python run.py

**Criar migração**  
alembic revision --autogenerate -m "Alterado tal informação"

**Executar migração**  
alembic upgrade head

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as variáveis de ambiente contidas no **.env_example**