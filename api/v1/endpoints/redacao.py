from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select 

from models.redacao_model import RedacaoModel
from core.deps import get_session


# Bypass warning SQlModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True # type: ignore
# Fim Bypass

# redacao_id é apenas para buscar o id no banco de dados
# db serve apenas para consultar no banco de dados determinados valores
# redacao: RedacaoModel ja serve para fazer alterações no banco de daddos


router = APIRouter()

# POST Redacao
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RedacaoModel)
async def post_redacao(redacao: RedacaoModel, db: AsyncSession = Depends(get_session)):
    nova_redacao = RedacaoModel(titulo=redacao.titulo, introducao=redacao.introducao, desenvolvimento1=redacao.desenvolvimento1, desenvolvimento2=redacao.desenvolvimento2, desenvolvimento3=redacao.desenvolvimento3, conclusao=redacao.conclusao)
    
    db.add(nova_redacao)
    await db.commit()
    
    return nova_redacao





# GET Redações
@router.get('/', response_model=List[RedacaoModel])
async def get_redacoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RedacaoModel)
        result = await session.execute(query)
        redacoes: List[RedacaoModel] = result.scalars().all()
        
        return redacoes
    




# GET Redação
@router.get('/{redacao_id}', response_model=RedacaoModel, status_code=status.HTTP_200_OK)
async def get_redacao(redacao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RedacaoModel).filter(RedacaoModel.id == redacao_id)
        result = await session.execute(query)
        redacao: RedacaoModel = result.scalar_one_or_none()
        
        if redacao:
            return redacao
        else:
            raise HTTPException(detail="Redação não encontrada", status_code=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
# PUT Redação        
@router.put('/{redacao_id}', status_code=status.HTTP_202_ACCEPTED, response_model=RedacaoModel)
async def put_redacao(redacao_id: int, redacao: RedacaoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RedacaoModel).filter(RedacaoModel.id == redacao_id)
        result = await session.execute(query)
        redacao_put: RedacaoModel = result.scalar_one_or_none()
        
        if redacao_put:
            redacao_put.titulo = redacao.titulo
            redacao_put.introducao = redacao.introducao
            redacao_put.desenvolvimento1 = redacao.desenvolvimento1
            redacao_put.desenvolvimento2 = redacao.desenvolvimento2
            redacao_put.desenvolvimento3 = redacao.desenvolvimento3
            redacao_put.conclusao = redacao.conclusao
            
            await session.commit()
            # serve para atualizar no banco
            return redacao_put
        else:
            raise HTTPException(detail="Redação não encontrada", status_code=status.HTTP_400_BAD_REQUEST)
        






# DELETE Redação
@router.delete('/{redacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_redacao(redacao_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RedacaoModel).filter(RedacaoModel.id == redacao_id)
        result = await session.execute(query)
        redacao_del: RedacaoModel = result.scalar_one_or_none()
        
        if redacao_del:
            await session.delete(redacao_del)
            # serve para atualizar no banco
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Redação não encontrada", status_code=status.HTTP_400_BAD_REQUEST)
        
