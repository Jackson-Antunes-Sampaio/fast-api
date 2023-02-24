from typing import Optional
from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras.')
        if value.islower():
            raise ValueError(' O titulo deve ser capitalizado.')
        return value


cursos = [
    Curso(id=1, titulo="Programação pra leigos", aulas=112, horas=58),
    Curso(id=2, titulo="Algoritmos e Lógicas da Programação", aulas=87, horas=67),
]
