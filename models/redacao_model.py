from typing import Optional

from sqlmodel import Field, SQLModel

class RedacaoModel(SQLModel, table=True):
    __tablename__: str = 'redacoes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    introducao: str
    desenvolvimento1: str
    desenvolvimento2: str
    desenvolvimento3: str
    conclusao: str
    
#  se eu colocar True ele cria no banco de dados a tabela em table=True se estiver em False consigo utilizar sem precisar salvar no banco ideal para testes antes de ir para produção

# Diferente do sqlalchemy o sqlmodel pode tratar tanto o mesmo model como schema ou model no banco de dados.