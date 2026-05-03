from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1/alunos", tags=["Alunos"])
service = AlunoService()


@router.post("/", response_model=Aluno, status_code=201)
def cadastrar_aluno(aluno: AlunoCreate):
    """Cadastra um novo aluno."""
    return service.criar(aluno)


@router.get("/", response_model=list[Aluno])
def listar_alunos():
    """Lista todos os alunos cadastrados."""
    return service.listar()


@router.get("/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: str):
    """Busca um aluno pelo ID (ex: GES1, GEC2)."""
    aluno = service.buscar_por_id(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.patch("/{aluno_id}", response_model=Aluno)
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate):
    """Atualiza parcialmente os dados de um aluno."""
    aluno = service.atualizar(aluno_id, dados)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: str):
    """Remove um aluno pelo ID."""
    sucesso = service.deletar(aluno_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": f"Aluno {aluno_id} removido com sucesso"}


@router.delete("/")
def resetar_alunos():
    """Reseta (apaga) toda a lista de alunos."""
    service.resetar()
    return {"mensagem": "Lista de alunos resetada com sucesso"}