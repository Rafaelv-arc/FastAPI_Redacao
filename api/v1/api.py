from fastapi import APIRouter

from api.v1.endpoints import redacao

# tags serve para agrupar os endpoints na documentação da API no caso vão se agrupar em redações

api_router = APIRouter()
api_router.include_router(redacao.router, prefix='/redacoes', tags=['redacoes'])
