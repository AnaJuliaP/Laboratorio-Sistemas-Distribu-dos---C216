from pydantic import BaseModel, EmailStr
from typing import Literal

CURSOS = Literal["GES", "GEC", "GTI", "GAD"]

class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: CURSOS

class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    curso: CURSOS | None = None

class Aluno(BaseModel):
    id: str
    matricula: int
    nome: str
    email: str
    curso: str