from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from models import Curso, cursos
from typing import List, Optional, Any, Dict
from time import sleep
from fastapi import Depends

# python main.py EXECUTAR APP
# pip install -r requerement.txt INSTALAR TODAS AS LIB DE UM PROJETO
# venv/Scripts/activate ATIVAR MAQUINA VIRTUAL
# deactivate DESATIVAR MAQUINA VIRTUAL
# python -m venv venv CRIAR MAQUINA VIRTUAL
# pip install fastapi psycopg2-binary sqlchemy asyncpg uvicorn CRIAR UM PROJETO COM BANCO DE DADOS
# pip freeze > requirements.txt MOSTRAR BICLIOTECAS INSTALADAS


def fake_db():
    try:
        print("ABRINDO CONEXÃO COM O BANCO DE DADOS...")
        # sleep(1)
    finally:
        print("FECHANDO CONEXÃO COM O BANCO DE DADOS...")
        # sleep(1)


app = FastAPI(title='API DE TESTE',
              version='0.0.1',
              description='Uma api para estudo do fast api',)


@app.get('/cursos',
         description='Retorna todos os cursos ou uma lista vazia.',
         summary='Retorna todos os cursos',
         response_model=List[Curso],
         response_description='Cursos encontratos com sucesso')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID DO CURSO', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')


@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso
    # else:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail=f"Já existe um curso com o ID {curso.id}")


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):

    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Não existe um curso com id {curso_id}')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, )
        return Response(status_code=status.HTTP_204_NO_CONTENT, )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Não existe um curso com id {curso_id}')


@app.get('/calculadora')
async def calcular(a: float = Query(default=None, gt=5), b: float = Query(default=None, gt=10), c: Optional[float] = 0, x_geek: str = Header(default=None)):
    resultado = a + b + c
    print(f"X-GEEK: {x_geek}")
    return {"resultado": resultado}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                log_level="info", reload=True)
